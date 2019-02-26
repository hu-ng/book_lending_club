# Welcome to the Book Lending Club

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
