import ckan.plugins as p
import ckan.plugins.toolkit as tk
import logging
import urllib
import urllib2

from pylons import config

log = logging.getLogger(__name__)


class RedlinkPreview(p.SingletonPlugin):
    """This extension previews data hosted on Redlink. """
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IResourcePreview, inherit=True)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)

    redlink_dataset = ''
    redlink_sparql = ''
    supported_formats = ['sparql', 'squebi']

    ## ITemplateHelpers
    def get_helpers(self):
        return {'sparql': self.redlink_sparql}

    ## IConfigurer
    def update_config(self, config):
        p.toolkit.add_public_directory(config, 'theme/public')
        p.toolkit.add_template_directory(config, 'theme/templates')
        p.toolkit.add_resource('theme/public', 'ckanext-redlink')


    def can_preview(self, data_dict):
        resource = data_dict['resource']
        format_lower = resource['format'].lower()
        if format_lower in self.supported_formats:
            return {'can_preview': True, 'quality': 2}

        return {'can_preview': False}


    def preview_template(self, context, data_dict):

        return 'redlink.html'

    def setup_template_variables(self, context, data_dict):
        """Get the dataset and SPARQL query for the current resource and bind them
        to the template variables."""
        dataset = data_dict['resource']['redlink_dataset']
        sparql = data_dict['resource']['redlink_sparql']

        tk.c.redlink_dataset = dataset
        tk.c.redlink_sparql = sparql

    ## IRoutes
    def after_map(self, map):
        log.info('after_map')
        controller = 'ckanext.redlink.plugin:RedlinkController'
        map.connect('/redlink/:dataset', controller=controller, action='redlink')

        return map

def dump(obj):
    for attr in dir(obj):
        print "obj.%s = %s" % (attr, getattr(obj, attr))


class RedlinkController(p.toolkit.BaseController):
    def redlink(self, environ, dataset):
        # The client may request different response formats. The format is set in the Accept header.
        # We get the Accept header from the request and copy it to the request we relay to the remote
        # server.

        accept = environ.get('HTTP_ACCEPT', 'NOT SET')
        headers = {'Accept': accept}

        app_key = config.get('redlink.app.key', '')  # Get the application key set in the configuration.

        log.info('redlink [ dataset :: {} ]'.format(dataset))
        url = 'https://api.redlink.io/1.0-BETA/data/' + dataset + '/sparql/select?key=' + app_key

        log.info('Posting request [ url :: {} ]'.format(url))

        # The client is sending the SPARQL statement as the request body. Since we're going to send a
        # url-encoded POST, we need to copy it to the query key.

        values = {'query': tk.request.body}

        data = urllib.urlencode(values)
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)

        return response.read()
