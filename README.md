#Project: Catalog App 


##Files and Directories Downloaded

Within the download you'll find the following directory and files:

catalog/
├── tournament.py
├── tournament.sql
├── tournament_test.py


##Required Libraries and Dependencies

* Make sure you have `python` installed [requires Python v2.7 to be installed]
* Requires 'Vagrant VM' to be installed and configured


##How to Run Project

### Run the virtual machine!

* Using the terminal, change directory to catalogofthings (**cd catalogofthings**)
* Type **vagrant up** to launch your virtual machine. 

### Run the Catalog App

* Once the Virtual Machine is up and running, type **vagrant ssh**
* Change to the /vagrant directory by typing **cd /vagrant**
* Type **ls** to ensure that you are inside the directory that contains application.py, database_setup.py, lotsofcategories.py, userslotsofcategories.py and  two directories named 'templates' and 'static'
* Type **python database_setup.py** to initialize the database.
* Type **python userslotsofcategories.py** to populate the database with users, categories and category items. (Optional)
* Type **python application.py** to run the Flask web server. In your browser visit **http://localhost:8000** to view the restaurant menu app. You should be able to view, add, edit, and delete categories and category items.
* When you want to log out, type **exit** at the shell prompt.


##Miscellaneous

To log into Facebook and Google, must create own app on their developer pages as my client secrets won't work here
