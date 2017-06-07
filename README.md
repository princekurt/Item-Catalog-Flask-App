# Item-Catalog-Flask-App
An online catalog app that uses Python with Flask and SQLAlchemy to perform CRUD operations on a database.
This project was designed using Python3.

# Installation
This app requires a linux server to run successfully. To develop the piece of software, a vagrant virtual machine was used. 
This vagrant machine was created and configured by Udacity and was run using Virtualbox on my machine.  
Steps:
1. Download Vagrant at Vagrantup.com  
2. Download Virtualbox at virtualbox.org  
3. Download the vagrant machine at https://github.com/udacity/fullstack-nanodegree-vm  
4. From a terminal, within the vagrant subdirectory run the command vagrant up
5. Once it's finished installing run vagrant ssh to log in  
6. The vagrant file on your desktop and within the machine are the same, copy the files you want to run into this directory and run them  
7. In our case, copy the file contents of this github inside, run the mainServer.py file

# Running the Program
Once you have the vagrant machine, or linux server of your choice running, run the mainServer.py file using python3.  
Open up a web browser and navigate to https://localhost:8000 to connect to the server. 

# Additional Requirements
This program uses a google client ID and secret ID specific to my subscription. You must sign up on Google API's to get your own
google client ID in order to have the google Authentication to work properly. 

# Authenticaiton
The app runs using OAuth2 authentication utilizing Google's API for this. To edit the database within the browser, you must be
logged in through the login button at the top of the page. Local permissions are also activated. This means that you cannot edit
something within the database that someone else has created. 
