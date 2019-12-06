import cherrypy

import os

import mimetypes

from cherrypy.lib import static

from utils import is_mobile_user_agent

from upload import Upload

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

