# Televisista Webex in HTML5 via SMS (NO APP) 
This repository is a template that can be used as a base to replicate the service os teleHealth. 

For this you will need the next things:
-A Webex with admin access to the control Hub
-Enough licenses to cover the medical acounts created
-A Twilio account 
-A webex Teams bot
-A Webex Guest Issuer 


## Instructions

This code is been developed in Pyhton Using th Flask Framework; with a mix of JS for the Frontend.
It is originally deployed in a Ubuntu VM with Python 3.7. the libraries and the version are represented in the reqs.txt file.
Within the file BashRunMe.sh are all the commands needed to set ready an Fresh Ubuntu VM; been an .sh file you can run it directly.
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
Workers: it is recommendes that you use between 2-4 workes per Core
Bind: the IP and port for the service(i reccomend that you use other than default 5000 port in flask)
run:app make reference to the name of the file (without the .py) and the module to run
access-logfile: the name of the to store the logs
error-logfile: the name of the file where the errors logs will be stored
capture-output: this force all the outputs to be store as error logs
D: this make the command to run as a Deamon

To generate the video call the browser will need to ask for acces to the micfofone an the camera; all the most user browser will need a valited Cert for this.

I recommend to use another service like NGNIX as a proxy and to provide the Cert.


