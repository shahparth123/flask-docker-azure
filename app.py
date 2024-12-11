from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/welcome/<name>')
def welcome(name):
    return render_template('home.html', name=name)

@app.route('/hello/<username>')
def hello_user(username):
    return f"Hello, {username}"

@app.route('/hello-user-id/<int:user_id>')
def hello_user_id(user_id):
    return f"User ID: {user_id}"

@app.route('/form', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        return f"Hello, {name}!"
    return render_template('form.html')

@app.route('/api/users', methods=['GET'])
def users():
    users= [{
        "user_id":1,
        "username":"parth"
    },{
    "user_id":2,
    "username":"ajit"
    }
    ]
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)