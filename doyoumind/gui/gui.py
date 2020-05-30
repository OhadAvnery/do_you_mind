import flask
from flask import Flask

def run_server(host, port, api_host, api_port):
    app = Flask(__name__, template_folder="react-app/build", static_folder="react-app/build/static")
    @app.route("/")
    @app.route('/<path:path>')
    def handle_path(path=None):
        return flask.render_template("index.html", api_host=api_host, api_port=api_port)    

    app.run(host=host, port=port)


run_server('127.0.0.1',8000,'127.0.0.1',5000)

#{{api_host}}, {{api_port}}