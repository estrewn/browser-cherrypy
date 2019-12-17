import MySQLdb
import cherrypy

import os

import time

from cherrypy.lib import static

from utils import is_mobile_user_agent

from upload import Upload

from stream import Stream

from video import Video

class Root(object):

    stream = Stream()

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

        secrets_file=open("/home/ec2-user/secrets.txt")

        passwords=secrets_file.read().rstrip('\n')

        db_password = passwords.split('\n')[0]
        
        dbname = "estrewn"

        conn = MySQLdb.connect(host='estrewn-production-instance-1.cphov5mfizlt.us-west-2.rds.amazonaws.com', user='browser', passwd=db_password, port=3306) 

        curs = conn.cursor()
        
        curs.execute("use "+str(dbname)+";")

        curs.execute("select unique_id from videos order by upload_time desc;")

        videos = curs.fetchall()

        for video in videos:

            assert(len(video) == 1)

            curs.execute("update videos set last_accessed_time = now(6) where unique_id="+str(video[0])+";")

            conn.commit()
            
            curs.execute("select IS_FREE_LOCK(\""+str(video[0])+"\")")

            isfreelock = bool(curs.fetchall()[0][0])
            
            doesfileexist = os.path.isfile('/home/ec2-user/videos/'+str(video[0])+'.mp4')
          
            while not (isfreelock and doesfileexist):

                time.sleep(1)
                
                curs.execute("select IS_FREE_LOCK(\""+str(video[0])+"\")")
                
                isfreelock = bool(curs.fetchall()[0][0])
                    
                doesfileexist = os.path.isfile('/home/ec2-user/videos/'+str(video[0])+'.mp4')

                if (isfreelock and doesfileexist):
                    break
                elif not doesfileexist and isfreelock:
                    curs.execute("select GET_LOCK(\""+str(video[0])+"\",10)")
                       
                    got_lock = bool(curs.fetchall()[0][0])

                    if got_lock:

                        curs.execute("select video from videos where unique_id="+str(video[0])+";")
                    
                        open('/home/ec2-user/videos/'+str(video[0])+'.mp4','w').write(curs.fetchall()[0][0])

                        curs.execute("select RELEASE_LOCK(\""+str(video[0])+"\")")

                        break

                        

        
        conn.close()
        
        video_html_string = ""
        
        for video in videos:

            assert(len(video) == 1)
            
            video_html_string += "<center><video width=\"640\" height=\"480\" controls>  <source src=\"/stream/?video_id="+str(video[0])+"\" type=\"video/mp4\"></video></center>"

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

"""+video_html_string+"""

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

<br>

<div class="divider"></div>

<br>

<center>This website is experimental at this point. You should expect bugs, unexpected downtime, etc. Please contact estrewn@gmail.com for comments, feature requests, etc.</center>

<br><br>

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

<div class="nonheader">

<div class="divider"></div>\n

<center><h1> Estrewn </h1></center>
<center><h3>A pile of digital content</h3></center>

"""+video_html_string+"""

</div>

<br>

<div class="divider"></div>

<br>

<center>This website is experimental at this point. You should expect bugs, unexpected downtime, etc. Please contact estrewn@gmail.com for comments, feature requests, etc.</center>

<br><br>

</body>
</html>

"""            
            
        return html_string

