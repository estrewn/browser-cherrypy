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

class Root(object):

    video = Video()
    
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True,
        'tools.sessions.locking': 'explicit', #this and the acquire_lock and the release_lock statements in the login and logout functions are necessary so that multiple ajax requests can be processed in parallel in a single session
        'response.stream': True
    }

    upload = Upload()
    
    @cherrypy.expose
    def index(self):

        is_mobile = False
        
        if "User-Agent" in cherrypy.request.headers and is_mobile_user_agent(cherrypy.request.headers['User-Agent']):
            is_mobile = True

        if is_mobile:    
            html_string = """
<html>

<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>
Estrewn
</title>

<style>

nav a, button {
    min-width: 48px;
    min-height: 48px;
}

html, body {
    height: 100%;
    width: 100%;
    margin-top:0;
    margin-left:0;
    margin-right:0;
}

a#menu svg {
    width: 40px;
    fill: #000;
}

main {
    width: 100%;
    height: 100%;
}

nav {
    width: 250px;
    height: 100%;
    position: fixed;
    transform: translate(-250px, 0);
    transition: transform 0.3s ease;
}

nav.open {
    transform: translate(0, 0);
}

.header {
float : right
}

.content {
padding-left:1em;
padding-right:1em;
}

.divider {
width:100%;
height:1px;
background-color:#dae1e9;
}

</style>

</head>

<body>

<nav id="drawer" style="background-color:LightGrey">
<center><h2 style="margin-top:0">Estrewn</h2></center>

<ul style="list-style:none;font-size:20px;padding-left:40px;">
<li style="padding-bottom:20px"><a href="/">Home</a></li>
<li style="padding-bottom:20px"><a href="/upload/">Upload</a></li>
</ul>

</nav>
<main>
<div style = "width:100%;top:0;left:0;">
<a id="menu">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <path d="M2 6h20v3H2zm0 5h20v3H2zm0 5h20v3H2z" />
  </svg>
</a>
<div class = "header">
<h1 style="margin-top:0;margin-bottom:0">Estrewn</h1>
</div>
</div>

<center><h1> Estrewn </h1></center>
<center><h3>A pile of digital content</h3></center>

<center>
<video width="640" height="480" controls>
  <source src="/video" type="video/mp4">
</video>
</center>

<script type="text/javascript" src="https://code.jquery.com/jquery-3.1.0.js"></script>
<script type="text/javascript">
var menu = document.querySelector('#menu');
var main = document.querySelector('main');
var drawer = document.querySelector('#drawer');
menu.addEventListener('click', function(e) {
    drawer.classList.toggle('open');
    e.stopPropagation();
});
main.addEventListener('click', function() {
    drawer.classList.remove('open');
});
main.addEventListener('touchstart', function() {
    drawer.classList.remove('open');
});
</script>    

</body>
</html>

"""
        else:

            html_string = """
<html>

<head>
<title>
Estrewn
</title>

<style>

.divider {
width:100%;
height:0.1em;
background-color:#dae1e9;
}

.nonheader { width:960px; margin: 80px auto 0px auto;  }

h1 { 
margin-top: 0.0em; 
margin-bottom: 0.0em; 
} 

h3 { 
margin-top: 0.0em; 
} 

.header1 {width:380px; float:left;}

.nav {
float: right;
padding: 20px 0px 0px 0px;
text-align: right;
}

header {background-color: White}

header {
position:fixed;
top:0px;
left:0px;
width:100%;
height:60px;
z-index:50;
}

.page{
width:960px; 
margin:0px auto 0px auto;
}

</style>
</head>

<body>

<header>
<div class = "page">
<div class = "header1">
<h1>Estrewn</h1>
<h3>A pile of digital content</h3>
</div>
<div class="nav">
<a href="/">Home</a> / <a href="/upload/">Upload</a> 
</div>
</div>
</header>

<div class=\"nonheader\">

<div class=\"divider\"></div>\n

<center><h1> Estrewn </h1></center>
<center><h3>A pile of digital content</h3></center>

<center>
<video width="640" height="480" controls>
  <source src="/video" type="video/mp4">
</video>
</center>
</div>
</body>
</html>

"""            
            
        return html_string

