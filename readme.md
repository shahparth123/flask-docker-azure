# Overview
1. Introduction to Flask
2. Routing and URL Parameters
3. Templates
4. Forms and Request Handling
5. API development
6. Preparing for deployment using Docker

## 1. Introduction to Flask
Flask is a lightweight web framework for Python, perfect for building web applications.

### Install Flask:
```bash
pip install flask
```

### Create your first flask application

Create a file called `app.py`

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)
```

Run this file using 
```bash
python app.py
```

This will create a webserver which will be accessible using `http://localhost:5000/` and opening that will show `Hello, Flask!` message.

## 2. Routing and URL Parameters
In flask you can define routes using `route` annotation on your function. You can also specify http methods in annotation as additional argument. By default method will be considered as `GET`.

You can pass any dynamic parameter in route using `<parameter>` syntex. If you want to typecast to something other then string you can use `<type:parameter>` syntex. 

So let's add few routes to our `app.py` before `if __name__ == '__main__':`

```python
@app.route('/hello/<username>')
def hello_user(username):
    return f"Hello, {username}"

@app.route('/hello-user-id/<int:user_id>')
def hello_user_id(user_id):
    return f"User ID: {user_id}"
```
This will add two routes to our application which you can access like `http://localhost:5000/hello/parth` and it will print `Hello, parth`

## 3. Templates
Webpages requires lengthy HTML, CSS, JS code to be embedded into pages. It will be difficult to write all that inside python functions. For improving that concept of templating is introduced.
Flask supports `Jinja2` syntex for templating.

Template directory structure will look like following:
```
project/
    app.py
    templates/
        home.html
```

We can create `home.html` file as follows:

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <title>Home</title>
</head>

<body>
    <h1>Welcome, {{ name }}!</h1>
</body>

</html>
```

and in `app.py` add following code
```python

from flask import render_template

@app.route('/welcome/<name>')
def welcome(name):
    return render_template('home.html', name=name)

```
On visiting `http://localhost:5000/welcome/parth` it will display html content of `hello.html` with name value of `parth`.

## 4. Forms and Request Handling
You can get input data using form with `GET` or `POST` http methods in flask using `request` module.
For that we will design a form which will be served using `GET` method and data of that form will be submitted using `POST` method.
So create `form.html` file in templates folder.

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <form method="POST" action="/form">
        <input type="text" name="name" placeholder="Enter your name">
        <button type="submit">Submit</button>
    </form>
</body>

</html>
```

In `app.py` add following code:
```python
from flask import request

@app.route('/form', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        return f"Hello, {name}!"
    return render_template('form.html') 
```

On visiting `http://localhost:5000/form` it will display form with input and on pressing submit it will display submitted data.

## 5. API development
If we want to design API which will be communicating with other services, it uses REST endpoints which utilizes JSON format for communication. 
Flask allows you to do that directly via `jsonify` method.

We can test that by adding following to `app.py`

```python
from flask import jsonify

@app.route('/api/users', methods=['GET'])
def users():
    users= [
        {
            "user_id":1,
            "username":"parth"
        },
        {
            "user_id":2,
            "username":"ajit"
        }
    ]
    return jsonify(users)

```

When you visit `http://localhost:5000/api/users` it will return data in JSON format.

## 6. Preparing for deployment using Docker
Till now we have run our application using development webserver which flask provide. But it is not scalable for large number of requests.

We can solve this issue by utilizing production web servers like `gunicorn` and deploying it to scalable docker containers.

For that lets create a file called `gunicorn_config.py` and add following:
```python
bind = "0.0.0.0:5000"
workers = 3  # Number of worker processes
threads = 2  # Number of threads per worker
timeout = 120
```
and create a `Dockerfile` with following content:
```Dockerfile
# Use Python 3.10 image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 5000

# Command to run the app using Gunicorn
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
```

Now we need to build the image form this dockerfile. 
In order to do that use following command from root of the project:
```bash
docker build -t demo-python-server .
```

And you can run it locally using following:

```bash
docker run -d -p 5000:5000 demo-python-server
```

Optionally you can publish to varioud docker registory by doing following:
```bash
docker build -t DOCKER_USERNAME/demo-python-server .
```

and 
```bash
docker push DOCKER_USERNAME/demo-python-server
```

### References
1. [https://flask.palletsprojects.com/en/stable/](https://flask.palletsprojects.com/en/stable/)
2. [https://gunicorn.org/](https://gunicorn.org/)
