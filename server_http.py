import cherrypy

class Root(object):

    @cherrypy.expose
    def default(self,*args):

        redirect_url = "https://estrewn.com"

        for arg in args:
            redirect_url = redirect_url+"/"+arg
            

        raise cherrypy.HTTPRedirect(redirect_url);

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 80})
    cherrypy.config.update({'server.socket_host': 'ec2-18-237-18-174.us-west-2.compute.amazonaws.com'})

    cherrypy.tree.mount(Root())
    cherrypy.engine.start()
    cherrypy.engine.block()

