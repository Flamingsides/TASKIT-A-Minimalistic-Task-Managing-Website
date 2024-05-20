# TASKIT: An Online Task Managing Tool/Todo-list
#### Video Demo: https://youtu.be/CEiB1SkWfSc
Project Finished On: 29th December 2023
Written For CS50x: Introduction To Programming Course Final Project (https://cs50.harvard.edu/x/2023/project/)

## About The Project
### General Description
This online tool allows you to keep track of any tasks you might have allowing you to: add tasks, edit them, delete them, or complete them. Every task has a title and a priority index (a higher priority index entails a more important task). Task descriptions, albeit optional, may also be provided. Finally, the program also allows users to see a log of tasks added, edited, deleted, or completed in the `history` tab. That is, unless the user clears their history. 

The program also supports multiple users, requiring each to sign in with a case-insensitive unique username and a password that may **not** be an empty string. All input fields include data validation and redirect to a user-friendly error page in case of incorrect user entry; this page allows users to return to the original page.

### Features At A Glance
1. Registering and signing in
2. Displays all current tasks
3. Adding tasks with properties: `title`, `description`, and `priority`
4. Marking tasks as `Completed`
5. Discarding tasks using the `Delete` button
6. Includes User-friendly GUI with a calming nature background behind the main `div`
7. Allows users to view history of tasks `Added`/`Completed`/`Edited`/`Deleted`
8. Allow editing of the following task properties (`title`, `description`, `priority`)
9. Allows selection of which types of actions to display in the `history` tab
10. Allows clearing history permanently
11. Features data validation with friendly error messages as well as password encryption (hashing).

### Project Images
#### Login Page
![Login Page Image](https://github.com/Flamingsides/TASKIT-A-Minimalistic-Task-Managing-Website/assets/84507406/e4fabbca-aafd-449c-aca6-10c0360ec96a)

#### Tasks Dashboard
![Tasks Dashboard](https://github.com/Flamingsides/TASKIT-A-Minimalistic-Task-Managing-Website/assets/84507406/05f6fefe-468a-4279-8160-f128df5e0cb6)

#### Adding/Editing Tasks
![Adding/Editing Tasks](https://github.com/Flamingsides/TASKIT-A-Minimalistic-Task-Managing-Website/assets/84507406/a457dec6-3d23-4a8a-818a-f0ebfe87ea9e)

####  Tasks History Tab
![Task History Tab](https://github.com/Flamingsides/TASKIT-A-Minimalistic-Task-Managing-Website/assets/84507406/f3299727-ee30-4e46-9a32-a743b14d09c9)

<style>
img {
    width: 50%;
}
</style>

### Technologies Used
#### Frontend
1. HTML
2. CSS
#### Backend
1. Python (Flask) - this was mostly used
2. Javascript
#### Database
* SQL (interacted with using CS50's library)

### The Motivation Behind Building This Project
As someone who finds himself swarmed with tasks daily and as someone that happens to have befriended many like himself, I found the prospect of building this project quite exciting indeed. I saw it as an opportunity to buld something I could use, something that would outlive the tenure of the course and would genuinely assist me in my day-to-day work. Granted, many such tools exist, I decided to give it my own touch. There is something unexplainably pleasing about using a tool you know you have made and a tool you know the ins and outs of.
To put it simply, TASKIT provides a simplistic GUI that allows tracking tasks - something I along with many that I know require.

### Reflection
Completing this project taught me how to plan out programming ventures before starting. Furthermore, I got more comfortable using all the technologies that assisted in the making of the website. I also found myself debugging quite frequently which is always a nice way to learn about the intricacies that are involved in some elements of a programming language. Last but definitely not least, I discovered that one's initial solution to a problem might not be the best or even correct. It is only through testing and pondering of different methods that the "best" methods comes to light.

## About The Author
### Author's Details
Name: Suhaib Hameed Zuberi
Age: 19
Nationality: Pakistani
Country Of Residence: Malaysia
Highest Qualification: IGCSE
Currently Enrolled In: Heriot-Watt University Malaysia's Foundation in Science (leading to Computing Science) course (Sem 2)
Holds Experience the Following Lanuages: C, C++, Python, Java, Javascript, Appscript (Basic), HTML, CSS, Scratch.

### Author's Socials
LinkedIn: https://www.linkedin.com/in/suhaib-hameed-zuberi/
GitHub: https://github.com/Flamingsides
Email Address: suhaib.zuberi2@gmail.com

## Detailed Analysis/Explanation of Files Written and Technologies Used
### Database (SQL) Structure
Storing Users:
```
CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    hash INTEGER NOT NULL
);
```
_Each user has a unique username and a hash of their password_

Storing Tasks:
```
CREATE TABLE tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    priority REAL NOT NULL CHECK (priority >= 0 AND priority <= 10),
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```
_Each task has a title, description, and priority. It also contains a Foreign Key referring to the owner of the task._

Logging History:
```
CREATE TABLE history(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    action TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    priority REAL NOT NULL CHECK (priority >= 0 AND priority <= 10),
    user_id INTEGER NOT NULL,
    time TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```
_Each log contains the type of action taken (`Added`/`Edited`/`Completed`/`Deleted`) along with the time of the log_
_Note: each log contins a copy of the task details instead of a `task_id` since the table tasks is not guaranteed to have each task stored forever._

The following unqiue index was created with the fact in mind that most queries to the database would reference the user's id
```
CREATE UNIQUE INDEX id ON users(id);
CREATE INDEX user_id ON tasks(user_id);
```

### Templates (HTML Files)
1. `add_task.html`
2. `clear_history.html`
3. `edit_task.html`
4. `error.html`
5. `history.html`
6. `layout.html`
7. `login.html`
8. `register.html`
9. `tasks.html`

> All .html files inherit from layout.html which includes the basic layout of the page. See below for how all the pages contribute.

#### Template: `add_task.html`
This file contains the interface for adding a new task, including the input boxes for the title and description of the task as well as a range input for the priority index of a task. Finally, there is a link to return to the tasks page without adding the task and an `Add Task` button; this sends a POST request to `/addtask`.

#### Template: `clear_history.html`
This file is served when the user wishes to delete all history. It presents the user with a warning and confirmation before proceeding and offers a `Cancel` button (link) and a `Clear All Data` button.

#### Template: `edit_task.html`
This file contains a very similar layout to the `add_task.html` file. It is served when the user wishes to edit an existing task.It also contains the same input fields; however, it also has a hidden input field whose value is the task's id in the database. This is retreived from the GET request and is kept to be submitted to in the POST request (to `/edittask`) once the `Save` button is clicked to submit.

#### Template: `error.html`
This file provides a friendly interface to display errors. It takes in an error message using Jinja syntax and a "return url" which the `Try Again` button (link) directs to.

#### Template: `history.html`
This file contains a table which displays all the contents of the `history` table in the SQL database. The table is set to overflow and allow horizontal scrolling when the screen size gets too slim. Additionally, it also contains a number of checkboxes for each "action" type (`Added`, `Edited`, `Completed`, `Deleted`) to indicate which logs to display; these are read by `script.js` which is discussed later in the file. Finally, there is also a `Clear History` button (link) on the far right of the checkboxes which leads to `clear_history.html`

#### Template: `layout.html`
This file contains the general layout of each webpage as each page inherits from this file. It contains a navbar on the top, the elements of which depend on whether the user is logged in or not. It also contains the background image a white div in the center where the the program's main action lies.

#### Template: `login.html`
This file contains a simple login page with textboxes for the user's username and password and a submit button to log in; this leads a POST request to `/login`.

#### Template: `register.html`
This file contains a simple register page with textboxes for the user's username, double entry of the password, and a `Register` button which submits a POST request to `/register`

#### Template: `tasks.html`
This template is served as the main dashboard. It contains a table which shows the contents of the `tasks` table from the database. The top left of the table contains the `Add Task` button which leads to `/addtask`. Furthermore, each row contains three buttons: `Edit` - leads to `/edit?id=TASK_ID` where `TASK_ID` is a task's id set using Jinja syntax, `Delete` - leads to `/delete?id=TASK_ID` where `TASK_ID` is set using Jinja syntax upon creating of the table, `Complete` - leads to `/complete?id=TASK_ID` where `TASK_ID` is as before.

### Static Folder
#### File: `styles.css`
This file defines CSS styles for the website.
Namely,
1. body styles which set the background image and center text alignment
2. `.main` class styles which sets the div in the center of `layout.html` where the main html of each file is rendered.
3. `.options-header` which defines the div above the table in `history.html` used to contain the `Clear History` button and the checkboxes to the right
4. `.show-history-type` which defines the div that houses the checkboxes that control which log types to show

#### File: `script.js`
Although the bulk of the logic lies in Python (Flask), some Javascript has been used for efficiency. The entirety of the Javascript has been wrapped in one event listener which listens for `DOMContentLoaded` to ensure the JS code runs only after the DOM tree has been built. Two main things are accomplished within scripts.js

##### First: Reflecting Value of Range Input on Pages `add_task.html` and `edit_task.html`
First of all, the range input that appear on the `edit_task.html` and `add_task.html` pages is searched for. If it exists, `eventListeners` are added which listen for a change in the range input bar and update the label above the range input to reflect the input's current value.

##### Second: Reflecting Value of Range Input on Pages `add_task.html` and `edit_task.html`
Second of all, an array is defined with all the types of logs named `logTypes`. This is relavent to just `history.html`. Next, an array is defined to contain all the types of logs which should be displayed in the history table. It is worth noting that the type of log refers to the type of action is represents (`Added`, `Edited`, `Completed`, `Deleted`). Subsequently, a function is declared (`updateHistory`) which updates the history tables to only show logs of which the type is found within the array `enabledTypes`, and hide all others using CSS `display: none;`. Finally, all check buttons are retreived. If they are found, eventListeners are added to them where are they detect change, their status is read. If checked, their value is added to the array `enabledTypes`, otherwise it is removed. _Note: a while loop is used in case multiple values have been added to the array somehow, like when a webpage is edited using editor tools_. At last, the `updateHistory` function is called to reflect the new changes.

> This task was done using Javascript because it is much more efficient to hide elements on screen instead of querying the database over and over again to ask for only specific types of logs.

#### Folder: `imgs/`
This folder contains images used in the website including website icons and the background image.

### Main Flask program: `app.py`
#### Imports
```
# Used to communicate with database
from cs50 import SQL

# Used to work with Flask
from flask import Flask, render_template, redirect, session, url_for, request
from flask_session import Session

# Used for password hashing
from werkzeug.security import generate_password_hash, check_password_hash

# Used to declare helper functions as decorators 
from functools import wraps

# Used to get current datetime to record history logs
from datetime import datetime
```

> After the imports, some basic configuration of the database and Flask sessions is conducted

#### Helper Functions
##### Decorator: `login_required(f)`
Used to ensure a user id is present in the current session before the function `f` is run. If not user is logged in, users are redirected to the login page.

##### Function: `error(message, return_url)`
Used to serve `error.html` to report an error or invalid input in a user-friendly manner. The user is presented with an error `message` as well as `Try Again` button which leads to `return_url` - this is usually the page where the user would be able to repeat their input.

##### Function: `log(action, title, description, priority)`
Used to update `history` table in the database. It inserts into the fields `action`, `title`, `description`, `priority` values passed in as positional arguments and into `user_id`, the id of the user currently logged in (`session["user_id"]`) and into time, the current time in the format `%Y-%m-%d %H:%M:%S` (using `datetime.now().strftime()`)

#### App Routes
There are a total of 11 routes;
1. `/`
2. `/tasks`
3. `/newtask`
4. `/complete`
5. `/delete`
6. `/edit`
7. `/history`
8. `/clearhistory`
9. `/register`
10. `/login`
11. `/logout`

Below is brief of their use.

##### Route: `/`
Methods Supported: `GET`

1. Redirects to `/tasks`.

##### Route: `/tasks`
Methods Supported: `GET`

1. Queries `tasks` table in database for tasks' titles, descriptions, and priorities
2. Serves `tasks.html`, passing in all data retreived from `tasks`.

##### Route: `/newtask`
Methods Suppoted: `GET`, `POST`

Upon a `GET` request,
1. Serves `add_task.html`

Upon a `POST` request,
1. Collects form data
2. Validates inpura
3. If valid, inserts the new task details into `tasks` in the database.
4. Logs the data using `log()`
5. Redirects to `tasks`

##### Route: `/complete`
Methods Supported: `GET`

1. Receives task id as an argument.
2. Validates task id
3. Logs task as `Completed`
4. Deletes task from `tasks` in database
5. Redirects to `/tasks`

##### Route: `/delete`
Methods Supported: `GET`

1. Receives task id as an argument.
2. Validates task id
3. Logs task as `Deleted`
4. Deletes task from `tasks` in database
5. Redirects to `/tasks`

##### Route: `/edit`
Methods Supported: `GET`,`POST`

Upon a `GET` request,
1. Receives task id as an argument.
2. Validates task id
3. Gets task details from `tasks` in database
4. Serves `edit_task.html` passing in task details

Upon a `POST` request,
1. Receives form data (task id, title, description, priority)
2. Valids new inputs
3. Updates `task` table in database
4. Logs task as `Edited`
5. Redirects to `/tasks`

##### Route: `/history`
Methods Supported: `GET`

1. Gets all logs from `history` table in database
2. Serves `history.html`, passing in data retreived from database

##### Route: `/clearhistory`
Methods Supported: `GET`, `POST`

Upon receiving a `GET` request,
1. Serves `clear_history.html`

Upon receiving a `POST` request,
1. Deletes all logs from `history` table with where the `user_id` matches logged-in user's id
2. Redirects to `/history`

##### Route: `/register`
Methods Supported: `GET`, `POST`

Upon receiving a `GET` request,
1. Serves `register.html`

Upon receiving a `POST` request,
1. Receives form data including username and password double entry
2. Validates input
3. Hashes password
4. Stores username and password hash in `users` table in the database
5. Redirects to `/login`

##### Route: `/login`
> This function was inspired by CS50's finance problem set.

Methods Supported: `GET`, `POST`

First of all, clears all session data in case there is old data still present.

Upon receiving a `GET` request,
1. Serves `login.html`

Upon receiving a `POST` request,
1. Retreives form data namely, username and password.
2. Validates inputs
3. Verfies inputs; _ensures username exists and password matches hash stored_
4. Stores user id in session upon successful login
5. Redirects to `/` (which currently redirects to `tasks`)

##### Route: `/logout`
> This function was inspired by CS50's finance problem set.

Methods Supported: `GET`

1. Clears all session data
2. Redirects to `/` (which would redirect to `/login` due to `@login_required` decorator)
