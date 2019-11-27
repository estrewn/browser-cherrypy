import MySQLdb
import datetime
import os
import cherrypy

import smtplib
import email

import mailbox

from email.MIMEMultipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.MIMEText import MIMEText

import time

import re

import random


import json

class Upload(object):
    @cherrypy.expose
    def index(self):

        is_mobile = False

        if "User-Agent" in cherrypy.request.headers and ("Android" in cherrypy.request.headers['User-Agent'] or "iPhone" in cherrypy.request.headers['User-Agent'] or "iPad" in cherrypy.request.headers['User-Agent']):
            is_mobile = True

        if is_mobile:

            html_string = """
<html>
<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>
Ecommunicate
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

<center><h2 style="margin-top:0">Ecommunicate</h2></center>

</nav>

<main>

<div style = "width:100%;top:0;left:0;">

<a id="menu">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <path d="M2 6h20v3H2zm0 5h20v3H2zm0 5h20v3H2z" />
  </svg>
</a>

<div class = "header">

<h1 style="margin-top:0;margin-bottom:0">Ecommunicate</h1>

</div>

</div>

<div class = "content">

<br>

<center>
   <form id="compose_email_form" target="console_iframe" method="post" action="send" enctype="multipart/form-data">
   video: <br><br>
   <input type="file" id="attachment1" name="attachment1"/>
   <br><br>
   title: <br><br>
   <input type="text" id="title" name="title" style="width:100%;border:2px solid black;font-size:120%;outline:none;" /><br><br>
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

$('#attachment1').click(function(event) { $('#attachment2').css('display','block')  });
$('#attachment2').click(function(event) { $('#attachment3').css('display','block')  });
$('#attachment3').click(function(event) { $('#attachment4').css('display','block')  });
$('#attachment4').click(function(event) { $('#attachment5').css('display','block')  });
$('#attachment5').click(function(event) { $('#attachment6').css('display','block')  });
$('#attachment6').click(function(event) { $('#attachment7').css('display','block')  });
$('#attachment7').click(function(event) { $('#attachment8').css('display','block')  });
$('#attachment8').click(function(event) { $('#attachment9').css('display','block')  });
$('#attachment9').click(function(event) { $('#attachment10').css('display','block')  });


$('#compose_email_form').submit(function(event) {

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

            $('#compose_email_form').hide();

            var console_iframe = document.getElementById('console_iframe');

            console_iframe.contentWindow.document.open();
            console_iframe.contentWindow.document.close();

            console_iframe.contentWindow.document.write('<center style="color:blue;font-size:20px;font-weight:bold">'+"E-mail sent succesfully."+'</center>');

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

        console_iframe.write("Error. E-mail not sent succesfully.");
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

</style>
<title>Ecommunicate</title>
</head>
<body>
<div class = "nonheader">

<center>
   <form id="compose_email_form" target="console_iframe" method="post" action="send" enctype="multipart/form-data">
   video: <br><br>
   <input type="file" id="attachment1" name="attachment1"/>
   <br><br>
   title: <br><br>
   <input type="text" id="title" name="title" size="100" /><br><br>
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
$('#attachment1').click(function(event) { $('#attachment2').css('display','block')  });

$('#compose_email_form').submit(function(event) {

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

            $('#compose_email_form').hide();

            var console_iframe = document.getElementById('console_iframe');

            console_iframe.contentWindow.document.open();
            console_iframe.contentWindow.document.close();

            console_iframe.contentWindow.document.write('<center style="color:blue;font-size:20px;font-weight:bold">'+"E-mail sent succesfully."+'</center>');

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

        console_iframe.write("Error. E-mail not sent succesfully.");
        //alert(JSON.stringify(data))
      }
   });


});

  </script>        
        </html>"""

        return html_string

    @cherrypy.expose
    def send(self, title, description, attachment1):

        attachments = [attachment1]

        def send_function():

            json_object = {}

            json_object["success"] = True

            json_object["errors"] = []

            if len(attachments) > 36:
                raise Exception

            dbname = "estrewn"

            secrets_file=open("/home/ec2-user/secrets.txt")
            passwords=secrets_file.read().rstrip('\n')
            db_password = passwords.split('\n')[0]

            conn = MySQLdb.connect(host='estrewn-production-instance-1.cphov5mfizlt.us-west-2.rds.amazonaws.com', user='browser', passwd=db_password, port=3306) 
            
            curs = conn.cursor()
            curs.execute("use "+str(dbname)+";")
            curs.execute("insert into videos values(%s,%s,now(6),%s)", ("a","b",MySQLdb.Binary(open("/home/ec2-user/1562534978890.mp4","rb").read())))
            conn.commit()
            
            print json.dumps(json_object)
            return json.dumps(json_object)
              
        return send_function()
