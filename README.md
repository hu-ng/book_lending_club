# Project Description

This web application is created a class project to serve as a platform for students in Minerva to coordinate book lending by aggregating books available in the cities that students live in and providing a tool to help both borrowers and lenders organize their requests.

As part of the back-end team for the project, I implemented many functionalities and wrote barebones html files to test them. My biggest contribution is implementing the "transaction" flow - the whole process of borrowing a book from start to end, from initiating a request to confirming that the borrower has returned the book. In addition to writing code that changes data but also maintains the consistency of the database, I also implemented checks to make sure that users can only do what they are allowed to do, like making sure that borrowers don't have access to lender-specific actions (and vice versa), or that borrowers can't "spam" request a book.

# Welcome to the Book Lending Club



## Run Virtual Environment

Virtual environment is a key component in ensuring that the application is configured in the right environment

##### Requirements
* Python 3
* Pip 3

```bash
$ brew install python3
```

Pip3 is installed with Python3

##### Installation
To install virtualenv via pip run:
```bash
$ pip3 install virtualenv
```

##### Usage
Creation of virtualenv:

    $ virtualenv -p python3 venv

If the above code does not work, you could also do 

    $ python3 -m virtualenv venv

To activate the virtualenv:

    $ source venv/bin/activate

Or, if you are **using windows** - [reference source:](https://stackoverflow.com/questions/8921188/issue-with-virtualenv-cannot-activate)

    $ venv\Scripts\activate

To deactivate the virtualenv (after you finished working):

    $ deactivate

Install dependencies in virtual environment:

    $ pip3 install -r requirements.txt


## Setup MySQL

[Install MySQL](https://dev.mysql.com/doc/refman/5.7/en/installing.html)

To setup the MySQL database necessary for the project, first log into the local database with the following command:

    $ mysql -u root -p

_If the above command does not work, even after you installed MySQL successfully, [this is a common problem](https://stackoverflow.com/questions/5920136/mysql-is-not-recognised-as-an-internal-or-external-command-operable-program-or-b). In **Windows**, you may need to edit the following environmental variables - MYSQLHOME: ```C:\Program Files\MySQL\MySQL Server 5.0```, and Path: ```%MYSQL_HOME%\bin;``` (do adjust the appropriate version and directory for the first one)_

_Another potential problem is to forget the password that was specified during the installation. [The solution to this is here](https://dev.mysql.com/doc/refman/8.0/en/resetting-permissions.html), just be patient following each of the steps very carefully._



Create the database for the current project
    
    $ create database book_lending_club;
    $ use book_lending_club;

Insert the following code to initialize a table for user

```
CREATE TABLE users (
    id int NOT NULL PRIMARY KEY,
    email varchar(255),
    username varchar(255)
);
```

## Initialize Database with MySQL
To get all the tables to start working, at the project directory, please go to the python console:
```bash
$ python
```
And enter the following command
```bash
$ from app import db 
$ db.drop_all()
$ db.create_all() 
```

## Setup Environment Variables

Environment variables are crucial in protecting sensitive information like API keys and passwords from being pushed to the CLI. One recommended tool to quickly setup environment varaibles in your local repo is direnv.

To install direnv, simply run

    $ brew install direnv

If installation is successful, add the following line to your bash (~/.bashrc or ~/.bash_profile) file

    $ eval "$(direnv hook bash)"
    
Restart your terminal or source the bash file with:

    $ source ~/.bash_profile

Create a new file under the project directory

    $ touch .envrc

Add the following code to .envrc

```
export database_username=PUT YOUR USERNAME
export database_pwd=PUT YOUR PASSWORD
export database_host=localhost
export database_db=book_lending_club
```

Finally, run `direnv allow` to save all the changes.

(Note: In the worst case scenario for Windows users, [you may do something like this](https://www.youtube.com/watch?v=IolxqkL7cD8), as direnv is not available for Windows)

## Add demo user to db

Running utils.py will add a demo user into the application

    $ python3 utils.py
    
The login information is as follows:

username: xd@gmail.com
password: 111

## Project Architecture

Project architecture section introduces different models that help build up the functionality of the Book Lending Club and their relationship with each other.

### User Model

Every logged-in user of the Book Lending Club is an instance of this model. The User Model should cover some basic authentication functionalities including
- Registration
- Sign in
- Sign out
- Edit Authentication Information (Password/Email/Username...)

Other than that, it should also have the attributes of *books* and *lent* which represent the list of books held by the user available for borrowing and the list of books the user has lent.

To encourage users to return books on time and positively contribute to community, the model also includes the stars attribute which awards users every time they receive positive comment and punishes when they return the book late.

![Example UML](https://yuml.me/diagram/scruffy/class/[User|+books;+lent;+stars;+username;-password|+Login();+Logout();])

### Book Model

The book model contains two separate classes: meta_book and book.

Meta_book class serves the function of recording the metadata of a specific book including name, author, and number of pages. In contrast, book class inherits from the meta_book and represents each book copy of that "meta book". It contains attributes like availability, owner, conditions, and etc.

![Example UML](https://yuml.me/diagram/scruffy/class/[Meta_book|+name;+author;+numpages;+username;]^-[Book|+availability;+owner_id;+condition])

### Transaction Model

The transaction model tracks the status of a lending process between the owner and lender. It includes basic functionalities of updating the status of a transaction.

![Example UML](https://yuml.me/diagram/scruffy/class/[Transaction|+book_id;+lender_id;+borrower_id;+status;+issue;|+update_status();])
