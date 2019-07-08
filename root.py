import cherrypy

import os

import mimetypes

from cherrypy.lib import static


class Video(object):
    @cherrypy.expose
    def index(self):

        f = open("/home/ec2-user/1562534978890.mp4")
        size = os.path.getsize("/home/ec2-user/1562534978890.mp4")
        mime = mimetypes.guess_type("/home/ec2-user/1562534978890.mp4")[0]
        print(mime)
        cherrypy.response.headers["Content-Type"] = mime
        cherrypy.response.headers["Content-Disposition"] = 'attachment; filename="%s"' % os.path.basename("/home/ec2-user/1562534978890.mp4")
        cherrypy.response.headers["Content-Length"] = size
        
        BUF_SIZE = 1024 * 5
        
        def stream():
            data = f.read(BUF_SIZE)
            while len(data) > 0:
                yield data
                data = f.read(BUF_SIZE)
            
        return static.serve_file("/home/ec2-user/1562534978890.mp4","application/x-download", "attachment","mp4 file")

class Root(object):

    video = Video()
    
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True,
        'tools.sessions.locking': 'explicit', #this and the acquire_lock and the release_lock statements in the login and logout functions are necessary so that multiple ajax requests can be processed in parallel in a single session
        'response.stream': True
    }


    
    @cherrypy.expose
    def index(self):

        html_string = """
<html>
<head>
<title>
Estrewn
</title>
</head>


<body>

<center><h1> Estrewn </h1></center>
<center><h3>A pile of digital content</h3></center>

<center>
<video width="320" height="240" controls>
  <source src="/video" type="video/mp4">
</video>
</center>
</body>
</html>

"""
        return html_string

