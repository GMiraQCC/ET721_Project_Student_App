# ET721_Project_Student_App
## Introduction
The Student Learning Management App uses the Flask framework to implement a full-stack web application intended to enhance the student's learning experience, thereby boosting their productivity.

It's features include a task management system in the form of a "To-Do List" & a note management system in the form of an "Image Uploader", both with user-friendly interfaces for managing academic responsibilities, as well as an authentication system that allows for signing up, logging in & logging out.

## Setup & Running
Setup is simple as the user only needs to execute 3 commands in the root folder to appropriately prepare the environment.
1. `python3 -m pip install --upgrade pip`
2. `pip install flask`
3. `sudo apt install sqlite3 -y`

Once that is complete, running the project is as simple as it gets. From the same terminal environment in the root folder, the user merely needs to run `python app.py` & open the preview in a new browser tab.

## The File Structure
The app itself has a particular file structure that satisfies the Flask framework integration standards/best-practices for full-stack web applications. 

### /static/
**/static/uploads** is where notes in the form of images uploaded by the student live. Accepted file formats at this location include pngs, jpgs, jpegs & gifs.

**/static/script.js** implements all the JavaScript functions corresponding to some of the routes in app.py, all of which are required for proper functioning of the application.

**/static/style.css** implements the majority of the CSS styling in the project that gives the app its simple, elegant & easy-to-read interface. The design decisions & color schemes lend themselves to friendly user interactivity.

### /templates/
**/templates/** houses each of the html files associated with each page of the application.

**/templates/base.html** is the ultimate template which gives the application its consistent, dependable theme.

If you already have an account, you can log-in through a frontend form thanks to **/templates/login.html**. Otherwise, if you need to create your account for the first time, you are presented with an option to travel to **/templates/signup.html**.

**/templates/dashboard.html** is the frontend hub that links to the main features of the app: **/templates/tasks.html**, which stores the To-Do List frontend & **/templates/images.html**, which stores the Image Uploader frontend. The final link to the final file is **/templates/blog.html**. The link works although the feature has yet to be fully implemented.

### /
Upon returning to the root folder /, you'll find **auth.db**, **todo.db** & **img.db**. Each are links to sqlite3 databases critical to the proper functioning of the main features of the application.

Finally, **/app.py** is where all the Flask-compliant Python code that serves as the backbone of the application is actually stored. This file handles all the routing necessary to ensure that the RESTful API HTTP requests play well with the databases & that the frontend reflects the state of the application accurately & appropriately. It's essentially the brains of the operation that connects all the pieces of the puzzle together. Within the file, each of the routes has a convenient, short description in the form of a comment.

### /app.py Explained
But to shortly reiterate:

There exists a function to establish a connection to each auth.db, todo.db & img.db.

Following that is a route & a function for each (1) loading the login page as the root page, (2) validating the log-in details & (3) presenting the dashboard of the logged in user.

Each of the following are related to the task management system. There is a route & function for (1) loading the home page of the To-Do List application, (2) getting all the user's saved tasks, (3) adding a new task & (4) deleting a task.

The next route & function allows the user to access the currently underdeveloped blogs feature.

Each of the following are related to the note management system. There exists a couple lines of Python for ensuring proper image functionality. Afterwards, there is a route & function for (1) loading the home page of the Image Uploader application, (2) uploading a new image, (3) downloading an image, & (4) deleting an image.

At this point, there is a route & a function associated with (1) logging out & (2) signing up, then the last lines of code in this file allow the app to run.