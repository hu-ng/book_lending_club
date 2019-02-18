# 9am Team structure:

## Project lead
 - Alya
 
The project lead will coordinate between every team. If there is an issue in one team which needs 
another team to solve it, then the project manager will get involved. Expect the project 
manager to create lots of issues, and tasks on github.
Another key task of the project manager is ensuring that every week there is a 
new prototype for a user(s) to look at, and making sure that other students
For the final project submission, the project lead will submit a list of the issues 
created, highlight instances where they provided direction, and/or show specific
instances where they facilitated cross team communication.  The quality of the final
project will also have a greater weighting on the project manager's grade.


## Architect (& potentially a *very* rough prototype)
 - Kevin

The architect will have the final say on all architectural decisions (duh!). This
will start with the architect drawing up an initial design (preferably in UML, 
but can also include a preliminary prototype). They will be responsible for the 
database schema. This role is primarily focused on choosing the design of the
tech stack, and the design of backend elements.  It is important to note that
the architect *does not* have much input on the design of the frontend. For the 
final project submission the architect will submit an overview of the project's 
design, and highlight instances where they made design decisions which were 
appropriate for the rest of the team's skill level.  A clean design will be the 
hallmark of a strong architectural contribution. If the architect also 
implemented a rough prototype then they can submit the PR in which this rough 
prototype was merged into master.

## Web design:
 - Ewa
 - Henry

 The web design team will focus on wireframing the website and user flows. They
 will take the results of any user feedback and modify the wireframe to 
 incorporate that feedback.  An intuitive set of user flows will be the hallmark
 of a good web design team. If the website has a lot of functionality, but still 
 feels uncluttered then there has been excellent web design work. For the final 
 project submission, the web design team will submit their initial design, as
 well as detailing how user feedback was incorporated into later iterations of 
 the design.

## Front end
 - Jose
 - Juan
 - Henry

The front end team will build the HTML/CSS/JS side of the website. If the 
website matches the designs of the web design team, and looks beautiful, then
the frontend team has done a great job. For the final project, the front end 
team will submit a list of PRs pointing to code that they authored.

## Back end
 - Jason
 - Hung
 - Pepe
 - Vy

The backend team writes all the code for the server side. This will typically 
involve receiving requests, querying the database, and returning the appropriate
results. It could also involve running scheduled tasks, or long-running 
analytical tasks. If the backend is fast, the code easy to read, and all 
functionality has been implemented then the backend team has done a great job.
For the final project, the back end team will submit a list of PRs pointing to 
code that they authored.


## Devops
 - Juan
 - Viet Hoang

The devops team will make everyone else's lives easier. Whenever a PR is opened
all unit tests and integration tests should be automatically run. If a PR is 
merged to master, then there must be an easy (or even fully automated) way of 
getting the master branch deployed to production.  The devops team will be 
evaluated on how easy it is to automatically find regressions in new code, how 
easy it is to run a development environment, and how easy it is to deploy master
to production. For the final project, the devops team will submit a list of PRs 
pointing to code that they authored.

## Testing:
 - Ivanna
 - Simon

All code that is written should have accompanying unit tests. However there is
still scope for a team of testers. This team will write integration tests, and
will also create as many unit tests as is feasible. They should be striving to 
stress test the system. What happens if a user tries to view this page, without 
logging in? What happens if a user submits an order with 0 items in it?
What happens if a user submits an order with negative items in it?  The testing
team will closely monitor code coverage. For the final project, the testing team 
will submit a list of PRs pointing to code that they authored.

## PR Reviewers:
 - Kevin
 - Jose
 - Jason
 - Henry
 - Hung
 - Viet Hoang

Whenever code is submitted, it will need to be reviewed and (potentially) 
approved.  Only the approval from this list of PR reviewers will strictly allow
the code to be merged. PR reviewers also have the option of submitting other 
people's PRs for which they provided advice, and significantly improved the 
quality of code merged as a result.  Think of this a little like the "internal 
mentor" team!

