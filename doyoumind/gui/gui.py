import flask

def run_server(host, port, api_host, api_port):
    app = Flask(__name__, static_folder="build/static", template_folder="build")

    @app.route("/")
    def index():
        return flask.render_template("index.html", api_server=f"http://{api_host}:{api_port}")