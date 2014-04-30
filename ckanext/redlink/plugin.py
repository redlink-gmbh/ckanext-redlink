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

    redlink_dataset = ''
    supported_formats = ['redlink', 'squebi']


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
        RedlinkPreview.redlink_dataset = data_dict['resource']['redlink_dataset']
        log.info('preview_template [ dataset :: {} ]'.format(RedlinkPreview.redlink_dataset))
        return 'redlink.html'


    ## IRoutes
    def after_map(self, map):
        controller = 'ckanext.redlink.plugin:RedlinkController'
        map.connect('/redlink', controller=controller, action='redlink')

        return map


class RedlinkController(p.toolkit.BaseController):
    def redlink(self, environ):
        # The client may request different response formats. The format is set in the Accept header.
        # We get the Accept header from the request and copy it to the request we relay to the remote
        # server.

        accept = environ.get('HTTP_ACCEPT', 'NOT SET')
        headers = {'Accept': accept}

        app_key = config.get('redlink.app.key', '')  # Get the application key set in the configuration.

        dataset = RedlinkPreview.redlink_dataset
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
