import MySQLdb
import datetime
import os
import cherrypy

from utils import is_mobile_user_agent

import json

class Upload(object):
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

.terminal {
    border: none; 
    width: 100%;
}

.header {
    float : right
}

.content {
    padding-left:1em;
    padding-right:1em;
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

<div class = "content">

<br>

<center>
   <form id="upload_form" target="console_iframe" method="post" action="send" enctype="multipart/form-data">
   video: <br><br>
   <input type="file" id="attachment" name="attachment"/>
   <br><br>
   title: <br><br>
   <input type="text" id="title" name="title" style="width:100%;border:2px solid black;font-size:120%;outline:none;" /><br><br>
   username: <br><br>
   <input type="text" id="username" name="title" style="width:100%;border:2px solid black;font-size:120%;outline:none;" /><br><br>
   description: <br><br>
   <textarea name="description" rows="30" cols="120" style="width:100%;border:2px solid black;font-size:120%;outline:none;"></textarea> <br><br>
  <button id="send" type="submit">
  Upload
  </button>
  </form>
  <iframe name="console_iframe" id="console_iframe" class="terminal" /></iframe>
</center>

</div>

</body>
<script type="text/javascript" src="https://code.jquery.com/jquery-3.1.0.js"></script>
<script>

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


$('#upload_form').submit(function(event) {

var formdata = new FormData($(this)[0]); 

//for (var pair of formdata.entries()) {
//    alert(pair[0]+ ', ' + pair[1]); 
//}

   event.preventDefault();

   var $this = $(this);

   $.ajax({
      url: $this.attr('action'),
      type: 'POST',
      data: formdata,
      processData: false,
      contentType: false,
      success: function(data){

        json_object = JSON.parse(data)

        if (json_object["success"]) {

            $('#upload_form').hide();

            var console_iframe = document.getElementById('console_iframe');

            console_iframe.contentWindow.document.open();
            console_iframe.contentWindow.document.close();

            console_iframe.contentWindow.document.write('<center style="color:blue;font-size:20px;font-weight:bold">'+"Video uploaded successfully."+'</center>');

        }

        else {

            var console_iframe = document.getElementById('console_iframe');

            console_iframe.contentWindow.document.open();
            console_iframe.contentWindow.document.close();

            console_iframe.contentWindow.document.write('<center style="color:red;font-size:20px;font-weight:bold">'+json_object["errors"]+'</center>');

        }

      },
      error : function (data) {
        var console_iframe = document.getElementById('console_iframe');

        console_iframe.write("Error. Video not uploaded successfully.");
        //alert(JSON.stringify(data))
      }
   });


});

  </script>        

</html>

</body>

"""
        else:
         
            html_string = """<html>
<head>
<style>
.terminal {
border: none; 
width: 100%; 
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
<title>Estrewn</title>
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

<center>
   <form id="upload_form" target="console_iframe" method="post" action="send" enctype="multipart/form-data">
   video: <br><br>
   <input type="file" id="attachment" name="attachment"/>
   <br><br>
   title: <br><br>
   <input type="text" id="title" name="title" size="100" /><br><br>
   username: <br><br>
   <input type="text" id="username" name="username" size="100" /><br><br>
   <br><br>
   description: <br><br>
   <textarea name="description" rows="30" cols="120"></textarea> <br><br>
  <button id="send" type="submit">
  Upload
  </button>
  </form>
  <iframe name="console_iframe" id="console_iframe" class="terminal" /></iframe>
</center>

</div>

</body>
<script type="text/javascript" src="https://code.jquery.com/jquery-3.1.0.js"></script>
<script>

$('#upload_form').submit(function(event) {

var formdata = new FormData($(this)[0]); 

//for (var pair of formdata.entries()) {
//    alert(pair[0]+ ', ' + pair[1]); 
//}

   event.preventDefault();

   var $this = $(this);

   $.ajax({
      url: $this.attr('action'),
      type: 'POST',
      data: formdata,
      processData: false,
      contentType: false,
      success: function(data){

        json_object = JSON.parse(data)

        if (json_object["success"]) {

            $('#upload_form').hide();

            var console_iframe = document.getElementById('console_iframe');

            console_iframe.contentWindow.document.open();
            console_iframe.contentWindow.document.close();

            console_iframe.contentWindow.document.write('<center style="color:blue;font-size:20px;font-weight:bold">'+"Video uploaded successfully."+'</center>');

        }

        else {

            var console_iframe = document.getElementById('console_iframe');

            console_iframe.contentWindow.document.open();
            console_iframe.contentWindow.document.close();

            console_iframe.contentWindow.document.write('<center style="color:red;font-size:20px;font-weight:bold">'+json_object["errors"]+'</center>');

        }

      },
      error : function (data) {
        var console_iframe = document.getElementById('console_iframe');

        console_iframe.write("Error. Video not uploaded successfully.");
        //alert(JSON.stringify(data))
      }
   });


});

  </script>        
        </html>"""

        return html_string

    @cherrypy.expose
    def send(self, title, username, description, attachment):

        def send_function():

            json_object = {}

            json_object["success"] = True

            json_object["errors"] = []

            tmp_filename=os.popen("mktemp").read().rstrip('\n')
            open(tmp_filename,'wb').write(attachment.file.read());
            
            dbname = "estrewn"

            secrets_file=open("/home/ec2-user/secrets.txt")
            passwords=secrets_file.read().rstrip('\n')
            db_password = passwords.split('\n')[0]

            conn = MySQLdb.connect(host='estrewn-production-instance-1.cphov5mfizlt.us-west-2.rds.amazonaws.com', user='browser', passwd=db_password, port=3306) 
            
            curs = conn.cursor()
            curs.execute("use "+str(dbname)+";")
            curs.execute("insert into videos values(NULL,%s,%s,%s,now(6),%s)", (username,title,description,MySQLdb.Binary(open(tmp_filename,"rb").read())))
            conn.commit()

            curs.execute("SELECT LAST_INSERT_ID()")
            conn.commit()

            print "unique_id = "+str(curs.fetchall()[0][0])
            
            conn.close()
            
            print json.dumps(json_object)
            return json.dumps(json_object)
              
        return send_function()
