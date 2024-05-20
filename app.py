import os
if not 'PROMPT' in os.environ:
    import sys
    nullfile = open(os.devnull, 'w')
    sys.stdout = nullfile
    sys.stderr = nullfile


from cs50 import SQL
from flask import Flask, render_template, redirect, session, url_for, request
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps
from datetime import datetime

# Configure Flask application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./flask_session_cache"
Session(app)

# Configure database using CS50's api
db = SQL("sqlite:///tasks.db")


# Function decorator that ensures some user is logged in before function is run
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return wrapper


# Loads a user-friendly error template
def error(message, return_url):
    return render_template("error.html", message=message, return_url=return_url)


# Logs a change to history
def log(action, title, description, priority):
    db.execute(
        "INSERT INTO history (action, title, description, priority, user_id, time) VALUES (?, ?, ?, ?, ?, ?)",
        action,
        title,
        description,
        priority,
        session["user_id"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    )


# Reroutes the root page to the /tasks page
@app.route("/")
@login_required
def index():
    return redirect("/tasks")


# This is the main dashboard
@app.route("/tasks")
@login_required
def tasks():
    # Get all current (undone) tasks
    cur_tasks = db.execute(
        "SELECT * FROM tasks WHERE user_id = ? ORDER BY priority DESC",
        session["user_id"] 
    )
    
    # Display all the tasks
    return render_template("tasks.html", cur_tasks=cur_tasks)


# Adding a new task
@app.route("/newtask", methods=["GET", "POST"])
@login_required
def addTask():
    if request.method == "POST":
        # Get task details
        title = request.form.get("title")
        description = request.form.get("description")
        priority = request.form.get("priority")

        # Entering a title and priority is mandatory
        if not (title and priority):
            return error(
                "You must choose a Title and Priority for your task!", "/newtask"
            )

        # Task description is not mandatory. Default: "No description provided"
        if not description:
            description = "No description provided"

        # Type Check: priority
        try:
            priority = float(priority)
        except ValueError:
            return error("Invalid input for priority", "/newtask")

        # Range Check: priority        
        if priority > 10.0 or priority < 0.0:
            return error("Priority must be on a scale of 1.0 to 10.0", "/newtask")

        # Add the task to the database
        db.execute(
            "INSERT INTO tasks (title, description, priority, user_id) VALUES (?, ?, ?, ?)",
            title,
            description,
            priority,
            session["user_id"] 
        )

        # Record the change in the history (Log)
        log("Added", title, description, priority)
        
        # Redirect to dashboard
        return redirect("/tasks")
    
    # GET: present a page to enter task details
    return render_template("add_task.html")


# Completing tasks
@app.route("/complete")
@login_required
def complete():
    task_id = request.args.get("id")

    task = db.execute(
        "SELECT title, description, priority FROM tasks WHERE id = ? AND user_id = ?",
        task_id,
        session["user_id"] 
    )

    if not task_id or not task:
        return error("Task Not Found", "/tasks")
    
    # Log data
    task = task[0]
    log("Completed", task["title"], task["description"], task["priority"])
    
    # Delete task from database as it is no longer a task
    db.execute(
        "DELETE FROM tasks WHERE id = ? AND user_id = ?;", task_id, session["user_id"]
    )

    # Redirect to main dashboard
    return redirect("/tasks")


# Deleting tasks
@app.route("/delete")
@login_required
def delete():
    # Get task id
    task_id = request.args.get("id")

    # Query data base for that specific task id
    task = db.execute(
        "SELECT title, description, priority FROM tasks WHERE id = ? AND user_id = ?",
        task_id,
        session["user_id"] 
    )

    # If task id is blank or task not found
    if not task_id or not task:
        return error("Task Not Found", "/tasks")
    
    # Log data
    task = task[0]
    log("Deleted", task["title"], task["description"], task["priority"])
    
    # Delete task
    db.execute(
        "DELETE FROM tasks WHERE id = ? AND user_id = ?;", task_id, session["user_id"]
    )

    # Redirect to main dashboard
    return redirect("/tasks")


# Editing tasks
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # Get task details
        task_id = request.form.get("id")
        title = request.form.get("title")
        description = request.form.get("description")
        priority = request.form.get("priority")

        # Title and Priority are mandatory fields
        if not (title and priority):
            return error(
                "Must provide a title and priority level", "/edit?id=" + task_id
            )

        # Description is not mandatory; defaults to "No description provided"
        if not description:
            description = "No description provided"

        # Type Check: priority
        try:
            priority = float(priority)
        except ValueError:
            return error("Invalid input for priority", "/edit?id=" + task_id)

        # Range Check: priority
        if priority > 10.0 or priority < 0.0:
            return error(
                "Priority must be on a scale of 1.0 to 10.0", "/edit?id=" + task_id
            )
        
        # Update task details based on new inputs
        db.execute(
            "UPDATE tasks SET title = ?, description = ?, priority = ? WHERE id = ? AND user_id = ?",
            title,
            description,
            priority,
            task_id,
            session["user_id"] 
        )

        # Log action
        log("Edited", title, description, priority)
        
        return redirect("/tasks")
    
    # GET
    task_id = request.args.get("id")

    # Ensure task id has been provided
    if not task_id:
        return error("Task Not Found", "/tasks")

    task = db.execute(
        "SELECT id, title, description, priority FROM tasks WHERE id = ? AND user_id = ?",
        task_id,
        session["user_id"] 
    )

    if not task:
        return error("Task Not Found", "/tasks")

    print("Editing: task[0]: ", task[0])
    return render_template("edit_task.html", task=task[0])


@app.route("/history")
@login_required
def history():
    # Get all logs
    logs = db.execute(
        "SELECT * FROM history WHERE user_id = ? ORDER BY time DESC", session["user_id"]
    )

    # Present log data in a user-friendly manner
    return render_template("history.html", logs=logs)


# Clearing history
@app.route("/clearhistory", methods=["GET", "POST"])
@login_required
def clearHistory():
    if request.method == "POST":
        db.execute("DELETE FROM history WHERE user_id = ?", session["user_id"])
        return redirect("/history")

    # GET
    return render_template("clear_history.html")


# Registering a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get username and implement presence check
        username = request.form.get("username").lower()
        if not username:
            return error("No Username Provided", "/register")
        
        # Ensure username is not taken
        if db.execute("SELECT username FROM users WHERE username = ?", username):
            return error("Username already taken", "/register")

        # Ensure password is not an empty string (presence check)
        if not request.form.get("password").strip():
            return error("Password cannot be nothing", "/register")

        # Ensure password is entered a second time
        if not request.form.get("confirmation"):
            return error("Enter Password Twice!", "/register")

        # Calculate hash value using first password entry
        pass_hash = generate_password_hash(request.form.get("password").strip())
        
        # Compare to hash of second password entry
        if not check_password_hash(pass_hash, request.form.get("confirmation").strip()):
            return error("Passwords Don't Match!", "/register")

        # Register user
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?);", username, pass_hash
        )
    
        # Allow login
        return redirect("/login")

    # GET
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return error("No username provided", "/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("No password provided", "/login")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            request.form.get("username").lower() 
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return error("Invalid username and/or password", "/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # GET
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget all user data
    session.clear()

    # Redirect to homepage
    return redirect("/")

if __name__ == "__main__":
    app.run()
