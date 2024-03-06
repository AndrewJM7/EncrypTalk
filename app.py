from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from main.views import main_blueprint
from users.views import users_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(users_blueprint)

@app.route('/')
def index():
    return render_template('main/index.html')

# Bad request
@app.errorhandler(400)
def bad_request_error(error):
    return render_template('errors/400.html'), 400

# The server is refusing action
def forbidden_error(error):
    return render_template('errors/403.html'), 403

# The requested resource could not be found but may be available in the future
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


# An unexpected condition happened
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500


# Server is not ready to handle the request
@app.errorhandler(503)
def service_unavailable_error(error):
    return render_template('errors/503.html'), 503

if __name__ == "__main__":
    app.run()
