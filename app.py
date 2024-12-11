from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"


@app.route('/hello/<username>')
def hello_user(username):
    return f"Hello, {username}"

@app.route('/hello-user-id/<int:user_id>')
def hello_user_id(user_id):
    return f"User ID: {user_id}"

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)