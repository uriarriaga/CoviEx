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






### Cookiecutter Automated Repo Creation

This process uses [cookiecutter](https://github.com/audreyr/cookiecutter) to auto-generate the files for you. This is helpful if you create multiple use cases. 

> Note: This template assumes the BSD 3-Clause License, you can change it be other licenses afterwards if that is not what you want.


1. Issue this command `pip install cookiecutter` to get ready to use the template.
2. Use this command and answer the questions: `cookiecutter https://github.com/CiscoDevNet/code-exchange-repo-template`
3. Update the [README](./README.md), replacing the contents below as described in text within each section of the README. Feel free to combine or omit sections where appropriate. 
4. Update the [LICENSE](./LICENSE), replacing the file with the license selected for your code. See the *Licensing info* section of this README for more info. 
5. Delete these instructions and everything up to the _Project Title_ from the README.
6. Write some great software and [submit](https://developer.cisco.com/codeexchange/github/submit) it to Code Exchange and/or Automation Exchange.



#### Example 
```bash
use-cases$ cookiecutter https://github.com/CiscoDevNet/code-exchange-repo-template
project_name [my-awesome-devnet-code-exchange-project]: my-first-project
project_description [baseline DevNet Code Exchange Project]: New Things to come!
author_name [Your Name Here]: User Name
author_email [youremail@domain.com]: user@cisco.com
use-cases$ tree
.DS_Store                          devnet-code-exchange/              my-first-project/
cookiecutter-devnet-code-exchange/ 
use-cases$ tree my-first-project/
my-first-project/
├── LICENSE
├── NOTICE
└── README.md

0 directories, 3 files
use-cases$
```

### Manual Repo Creation

If you are only creating one use case, this process is probably easier. 

1. Create a new repository.
2. Copy all the files inside `manual-sample-repo` into your new repository. 
3. Update the [README](./README.md), replacing the contents below as described in text within each section of the README. Feel free to combine or omit sections where appropriate. 
4. Update the [LICENSE](./LICENSE), replacing the file with the license selected for your code. See the *Licensing info* section of this README for more info. 
5. Delete these instructions and everything up to the _Project Title_ from the README.
6. Write some great software and [submit](https://developer.cisco.com/codeexchange/github/submit) it to Code Exchange and/or Automation Exchange.

 