import logging
import ckan.plugins as p
import urllib
import urllib2
import ckan.plugins.toolkit as toolkit


from pylons import config

log = logging.getLogger(__name__)

try:
    import ckanext.resourceproxy.plugin as proxy
except ImportError:
    pass


class RedlinkPreview(p.SingletonPlugin):
    """This extension previews PDFs. """
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IConfigurable, inherit=True)
    p.implements(p.IResourcePreview, inherit=True)
    p.implements(p.IRoutes, inherit=True)

    supported_formats = ['redlink', 'squebi']
    app_key = 'AAA'
    proxy_is_enabled = False

    def update_config(self, config):
        p.toolkit.add_public_directory(config, 'theme/public')
        p.toolkit.add_template_directory(config, 'theme/templates')
        p.toolkit.add_resource('theme/public', 'ckanext-redlink')

    def configure(self, config):
        """Get the application key."""
        app_key = config.get('redlink.app.key', '')

        log.info('configure [ app key :: {0} ]'.format(app_key))

        self.app_key = app_key

        enabled = config.get('ckan.resource_proxy_enabled', False)
        self.proxy_is_enabled = enabled

    def can_preview(self, data_dict):
        resource = data_dict['resource']
        format_lower = resource['format'].lower()
        if format_lower in self.supported_formats:
            return {'can_preview': True, 'quality': 2}
            # if resource['on_same_domain'] or self.proxy_is_enabled:
            #     return {'can_preview': True, 'quality': 2}
            # else:
            #     return {'can_preview': False,
            #             'fixable': 'Enable resource_proxy',
            #             'quality': 2}
        return {'can_preview': False}

    def setup_template_variables(self, context, data_dict):
        if (self.proxy_is_enabled
                and not data_dict['resource']['on_same_domain']):
            url = proxy.get_proxified_resource_url(data_dict)
            p.toolkit.c.resource['url'] = url

    def preview_template(self, context, data_dict):
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

        url = 'https://api.redlink.io/1.0-BETA/data/events/sparql/select?key=' + app_key

        # The client is sending the SPARQL statement as the request body. Since we're going to send a
        # url-encoded POST, we need to copy it to the query key.

        values = {'query': toolkit.request.body}

        data = urllib.urlencode(values)
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)

        return response.read()
