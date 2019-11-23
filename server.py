import cherrypy

from root import Root

def redirect_if_authentication_is_required_and_session_is_not_authenticated(*args, **kwargs):

    conditions = cherrypy.request.config.get('auth.require', None)
    if conditions is not None:
        username = cherrypy.session.get('_cp_username')
        if not username:
            from_url = cherrypy.request.request_line.split()[1]

            raise cherrypy.HTTPRedirect("/loginlogout/login?from_page=%22"+from_url.replace('&&','%01').replace('%22','%00')+"%22")

cherrypy.tools.auth = cherrypy.Tool('before_handler', redirect_if_authentication_is_required_and_session_is_not_authenticated)

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 443}) #port 443 for https or port 80 for http
#    cherrypy.config.update({'server.socket_port': 80})
#    cherrypy.config.update({'server.socket_host': 'ec2-18-237-18-174.us-west-2.compute.amazonaws.com'})
    cherrypy.config.update({'server.socket_host': '10.0.0.136'})
    

    #cherrypy.tree.mount(Root())
    cherrypy.tree.mount(Root(),'/',

{ 

}

 )

    cherrypy.server.ssl_module = 'builtin'
    cherrypy.server.ssl_certificate = "/etc/letsencrypt/live/estrewn.com/fullchain.pem"
    cherrypy.server.ssl_private_key = "/etc/letsencrypt/live/estrewn.com/privkey.pem"
    cherrypy.server.ssl_certificate_chain = "/etc/letsencrypt/live/estrewn.com/fullchain.pem"
    cherrypy.server.thread_pool = 50


    cherrypy.engine.start()
    cherrypy.engine.block()

