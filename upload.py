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
   to: <br><br>
   <input type="text" id="to" name="to" style="width:100%;border:2px solid black;font-size:120%;outline:none;" /><br><br>
   cc: <br><br>
   <input type="text" id="cc" name="cc" style="width:100%;border:2px solid black;font-size:120%;outline:none;" /><br><br>
   subject: <br><br>
   <input type="text" id="subject" name="subject" style="width:100%;border:2px solid black;font-size:120%;outline:none;" /><br><br>
   attachments: <br><br>
   <input type="file" id="attachment1" name="attachment1"/>
   <input type="file" id="attachment2" name="attachment2" style="display:none;"/>
   <input type="file" id="attachment3" name="attachment3" style="display:none;"/>
   <input type="file" id="attachment4" name="attachment4" style="display:none;"/>
   <input type="file" id="attachment5" name="attachment5" style="display:none;"/>
   <input type="file" id="attachment6" name="attachment6" style="display:none;"/>
   <input type="file" id="attachment7" name="attachment7" style="display:none;"/>
   <input type="file" id="attachment8" name="attachment8" style="display:none;"/>
   <input type="file" id="attachment9" name="attachment9" style="display:none;"/>
   <input type="file" id="attachment10" name="attachment10" style="display:none;"/>
   <br><br>
   body: <br><br>
   <textarea name="body" rows="30" cols="120" style="width:100%;border:2px solid black;font-size:120%;outline:none;"></textarea> <br><br>
  <button id="send" type="submit">
  Send
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
   to: <br><br>
   <input type="text" id="to" name="to" size="100" /><br><br>
   cc: <br><br>
   <input type="text" id="cc" name="cc" size="100" /><br><br>
   subject: <br><br>
   <input type="text" id="subject" name="subject" size="100" /><br><br>
   attachments: <br><br>
   <input type="file" id="attachment1" name="attachment1"/>
   <input type="file" id="attachment2" name="attachment2" style="display:none;"/>
   <input type="file" id="attachment3" name="attachment3" style="display:none;"/>
   <input type="file" id="attachment4" name="attachment4" style="display:none;"/>
   <input type="file" id="attachment5" name="attachment5" style="display:none;"/>
   <input type="file" id="attachment6" name="attachment6" style="display:none;"/>
   <input type="file" id="attachment7" name="attachment7" style="display:none;"/>
   <input type="file" id="attachment8" name="attachment8" style="display:none;"/>
   <input type="file" id="attachment9" name="attachment9" style="display:none;"/>
   <input type="file" id="attachment10" name="attachment10" style="display:none;"/>
   <br><br>
   body: <br><br>
   <textarea name="body" rows="30" cols="120"></textarea> <br><br>
  <button id="send" type="submit">
  Send
  </button>
  </form>
  <iframe name="console_iframe" id="console_iframe" class="terminal" /></iframe>
</center>

</div>

</body>
<script type="text/javascript" src="https://code.jquery.com/jquery-3.1.0.js"></script>
<script>
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
        </html>"""

        return html_string

    @cherrypy.expose
    def send(self, to, cc, subject, attachment1, attachment2, attachment3, attachment4, attachment5, attachment6, attachment7, attachment8, attachment9, attachment10, body):

        attachments = [attachment1, attachment2, attachment3, attachment4, attachment5, attachment6, attachment7, attachment8, attachment9, attachment10]

        def send_function():

            json_object = {}

            json_object["success"] = True

            json_object["errors"] = []

            print "to:"
            print to
            print "cc:"
            print cc
            print "subject:"
            print subject
            print "body:"
            print body

            msg = MIMEMultipart()
            send_from = cherrypy.session.get('_cp_username')+"@ecommunicate.ch"
            #msg['From'] = 
            send_to = re.findall(r'[^\;\,\s]+',to)
            send_cc = re.findall(r'[^\;\,\s]+',cc)

            if to == "":
                json_object["success"] = False
                json_object["errors"].append("to is empty.")
                print json.dumps(json_object)
                return json.dumps(json_object)

            for email_address in (send_to + send_cc):
                if len(email_address.split("@")) != 2:
                    json_object["success"] = False
                    json_object["errors"].append("Each e-mail address must contain one @ symbol.")
                    print json.dumps(json_object)
                    return json.dumps(json_object)
                if email_address.split("@")[1] != "ecommunicate.ch":
                    json_object["success"] = False
                    json_object["errors"].append("Can only send e-mails to other ecommunicate.ch e-mail addresses.")
                    print json.dumps(json_object)
                    return json.dumps(json_object)

            msg['To'] = COMMASPACE.join(send_to)
            msg['CC'] = COMMASPACE.join(send_cc)
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = subject

            mime_applications = []

            l = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']

            if len(attachments) > 36:
                raise Exception

            for i,attachment in enumerate(attachments):
                if attachment.file != None and attachment.filename != "":
                    tmp_filename=os.popen("mktemp").read().rstrip('\n')
                    open(tmp_filename,'wb').write(attachment.file.read());
                    
                    if str(attachment.content_type) == "application/pdf":
                        mime_application = MIMEApplication(open(tmp_filename,'rb').read(),"pdf")
                        mime_application['Content-Disposition'] = 'attachment; filename="'+str(attachment.filename)+'"'
                        mime_application['Content-Description'] = str(attachment.filename)
                        mime_application['X-Attachment-Id'] = str("f_")+l[random.randint(0,35)]+l[random.randint(0,35)]+l[random.randint(0,35)]+l[random.randint(0,35)]+l[i]+l[random.randint(0,35)]+l[random.randint(0,35)]+l[random.randint(0,35)]+l[random.randint(0,35)]
                        mime_applications.append(mime_application)

            try:

                msg.attach(MIMEText(body))

                for mime_application in mime_applications:
                    msg.attach(mime_application)

                smtpObj = smtplib.SMTP(port=25)

                smtpObj.connect()

                smtpObj.sendmail(send_from, send_to+send_cc, msg.as_string())
                
                smtpObj.close()


            except Exception as e:
                print "Error: unable to send email", e.__class__

            print json.dumps(json_object)
            return json.dumps(json_object)
              
        return send_function()
