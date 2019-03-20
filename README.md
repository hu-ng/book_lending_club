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

To deactivate the virtualenv (after you finished working):

    $ deactivate

Install dependencies in virtual environment:

    $ pip3 install -r requirements.txt


## Setup MySQL

[Install MySQL](https://dev.mysql.com/doc/refman/5.7/en/installing.html)

To setup the MySQL database necessary for the project, first log into the local database with the following command:

    $ mysql -u root -p

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

![Example UML](https://yuml.me/diagram/scruffy/class/[Transaction|+book_id;+lender_id;+borrower_id;+status;|+update_status();])
