import ckan.plugins as p
import ckan.model as m
import ckan.plugins.toolkit as tk
import logging
import urllib
import urllib2
import re

from pylons import config, response

log = logging.getLogger(__name__)


class RedlinkPreview(p.SingletonPlugin):
    """This extension previews data hosted on Redlink. """
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IResourcePreview, inherit=True)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)

    redlink_dataset = ''
    redlink_sparql = ''
    redlink_key = ''
    supported_formats = ['sparql', 'squebi']

    ## ITemplateHelpers
    def get_helpers(self):
        return {'sparql': self.redlink_sparql}

    ## IConfigurer
    def update_config(self, config):
        p.toolkit.add_public_directory(config, 'theme/public')
        p.toolkit.add_template_directory(config, 'theme/templates')
        # p.toolkit.add_resource('theme/public/ckanext-redlink', 'ckanext-redlink')

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

        self.redlink_key = data_dict['package']['redlink_key']

        tk.c.redlink_dataset = dataset
        tk.c.redlink_sparql = sparql
        tk.c.redlink_key = data_dict['package']['redlink_key']

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

        context = {
            'model': m,
            'session': m.Session,
            'user': tk.c.user or tk.c.author,
            'auth_user_obj': tk.c.userobj,
        }

        #get the dataset id from the url
        dataset_id = re.search('http://data.salzburgerland.com/dataset/([\w-]+)/resource/([\w-]+)/preview',environ.get('HTTP_REFERER')).group(1)

        #get the dataset dictionary
        dataser_dict = tk.get_action('package_show')(context, {'id':dataset_id})

        # Get the application key from the dataset dictionary.
        app_key = dataser_dict['redlink_key']

        url = 'https://api.redlink.io/1.0/data/' + dataset + '/sparql/select?key=' + app_key + '&out=' + (tk.request.params.get('out', '') or '')

        log.info('redlink [ dataset :: {} ]'.format(dataset))
        log.info('redlink [ key :: {} ]'.format(app_key))
        log.info('Posting request [ url :: {} ]'.format(url))

        # The client is sending the SPARQL statement as the request body. Since we're going to send a
        # url-encoded POST, we need to copy it to the query key.

        values = {'query': tk.request.params.get('query', tk.request.body)}

        data = urllib.urlencode(values)
        req = urllib2.Request(url, data, headers)

        redlink_response = urllib2.urlopen(req)

        # Set the response content type to match Redlink's.

        response.content_type = redlink_response.info().getheader('Content-Type')

        return redlink_response.read()

class RedlinkIDatasetFormPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    """This plugin adds a Redlink app key to a data-set schema. """
    p.implements(p.IDatasetForm)

    redlink_key=''

    def _modify_package_schema(self, schema):
        schema.update({
            'redlink_key': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')]
        })
        return schema

    # Adds the app key field to the basic dataset schema on dataset creation time
    def create_package_schema(self):
        log.debug('Creating a new redlink dataset')
        schema = super(RedlinkIDatasetFormPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    # Adds the app key field to the basic dataset schema on dataset update time
    def update_package_schema(self):
        log.debug('Updating a redlink dataset')
        schema = super(RedlinkIDatasetFormPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    # Retrieves the app key field to the basic dataset schema on dataset show time
    def show_package_schema(self):
        schema = super(RedlinkIDatasetFormPlugin, self).show_package_schema()
        schema.update({
            'redlink_key': [tk.get_converter('convert_from_extras'),
                                tk.get_validator('ignore_missing')]
        })
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []
