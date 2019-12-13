import cherrypy

import os

import mimetypes

from cherrypy.lib import static

from utils import is_mobile_user_agent

from upload import Upload

class Stream(object):
    @cherrypy.expose
    def index(self,video_id):

        return static.serve_file("/home/ec2-user/videos/"+str(video_id)+".mp4","application/x-download", "attachment","mp4 file")

