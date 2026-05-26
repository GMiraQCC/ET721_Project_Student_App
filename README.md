# ET721_Project_Student_App
## Introduction
The Student Learning Management App uses the Flask framework to implement a full-stack web application intended to enhance the student's learning experience, thereby boosting their productivity.

It's features include a task management system in the form of a "To-Do List" & a note management in the form of an "Image Uploader", both with user-friendly interfaces for managing academic responsibilities, as well as an authentication system that allows for signing up, logging in & logging out.

## Setup & Running
Setup is simple as the user only needs to execute 3 commands in the root folder to appropriately prepare the environment.
1. `python3 -m pip install --upgrade pip`
2. `pip install flask`
3. `sudo apt install sqlite3 -y`

Once that is complete, running the project is as simple as it gets. From the same terminal environment in the root folder, the user merely needs to run `python app.py` & open the preview in a new browser tab.

## The File Structure
The app itself has a particular file structure that satisfies the Flask framework integration standards/best-practices for full-stack web applications. 

/static/uploads is where notes in the form of images uploaded by the student live. Accepted file formats at this location include pngs, jpgs, jpegs & gifs.
/static/script.js implements all the JavaScript functions corresponding to some of the routes in app.py, all of which are required for proper functioning of the application.
/static/style.css implements the majority of the CSS styling in the project that gives the app its simple, elegant & easy-to-read interface. The design decisions & color schemes lend themselves to friendly user interactivity.

Moving on, /templates/ houses each of the html files associated with each page of the application.
/templates/base.html is the ultimate template which gives the application its consistent, dependable theme.
If you already have an account, you can log-in through a frontend form thanks to /templates/login.html. Otherwise, if you need to create your account for the first time, you are presented with an option to travel to /templates/signup.html.
/templates/dashboard.html is the frontend hub that links to the main features of the app: /templates/tasks.html, which stores the To-Do List frontend & /templates/images.html, which stores the Image Uploader frontend.
The final file in /templates/ is blog.html. A working link to it exists in /templates/dashboard.html, but the feature hasn't been fully implemented.

Upon returning to the root folder /, you'll find auth.db, todo.db & img.db. Each are links to sqlite3 databases critical to the proper functioning of the main features of the application.

Finally, /app.py is where all the Flask-compliant Python code that serves as the backbone of the application is actually stored. This file handles all the routing necessary to ensure that the RESTful API HTTP requests play well with the databases & that the frontend reflects the state of the application accurately & appropriately. It's essentially the brains of the operation that comnects all the pieces of the puzzle together.
