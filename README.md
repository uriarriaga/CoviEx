# Televisista Webex in HTML5 via SMS (NO APP) 
This repository is a template that can be used as a base to replicate the teleHealth service. 

The objective of this document is to technically detail the Tele Consultation Application that is based on the Webex video conferencing engine and that is being used at INER
<br>The application aims to:
<br>• Generate accessibility for people who are not native to the digital age
<br>• Automate and facilitate the generation of communication channels between doctors, patients and relatives
<br>• Give full control of these communication channels to Health personnel
<br>• Integrate technologies such as HTML5, Webex, and SMS to achieve the above objectives

The way in which these objectives are achieved is through a Web page in which Health personnel can generate a Webex session; once this session has been generated, a link is sent via SMS with which relatives and patients can access the video conference without installing any application; This is accomplished using the Webex SDK for HTML5. The user only has to click 2 times to enter the session.

<img src="architecture.png" alt="architecture">

<img src="widget.png" alt="widget">


## Instructions

You will need next things to be able to use this Code:
<br>-A Webex with admin access to the control Hub
<br>-Enough licenses to cover the medical acounts created
<br>-A Twilio account 
<br>-A webex Teams bot
<br>-A Webex Guest Issuer 

This code is been developed in Pyhton Using th Flask Framework; with a mix of JS for the Frontend.

It is originally deployed in a Ubuntu VM with Python 3.7. the libraries and the version are represented in the reqs.txt file.

Within the file BashRunMe.sh are all the commands needed to set ready an Fresh Ubuntu VM; been an .sh file you can run it directly.

All the needed varibles must exist as environment variables . Either you add them via the CLI or you use the exampleDOTenv to create a .env file so that when run the code this add them automatically.

Once the VM is ready with  all the packages installed, python 3.7 and all the libries for python installed yo can just use the command:

```python
 python3 runme.py
 ```
This is NOT a recommended way leave it running, but you can use this to check that everything is ready.
Once everything is Ready I recommend that you use aome kind of WSGI service; in this case we will use Gunicorn.

if you run the bashRunMe.sh you should alredy get installed gunicorn; you can use the next command to keep it running:
```bash
gunicorn3 --workers=8 --bind 0.0.0.0:xxx run:app --access-logfile gunicorn.log --error-logfile gunicorn-error.log --capture-output -D
```
Let me explain a little bit datailed this command:
<br>Workers: it is recommendes that you use between 2-4 workes per Core
<br>Bind: the IP and port for the service(i reccomend that you use other than default 5000 port in flask)
<br>run:app make reference to the name of the file (without the .py) and the module to run
<br>access-logfile: the name of the to store the logs
<br>error-logfile: the name of the file where the errors logs will be stored
<br>capture-output: this force all the outputs to be store as error logs
<br>D: this make the command to run as a Deamon

To generate the video call the browser will need to ask for acces to the micfofone an the camera; all the most user browser will need a valited Cert for this.

I recommend to use another service like NGNIX as a proxy and to provide the Cert.

Contact Info:

joarriag@cisco.com

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/Momoyactly/PSdCloud)

