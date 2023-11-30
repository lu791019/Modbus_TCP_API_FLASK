"""WSGI config for AiSails project."""

from app import create_app
from app.blueprint import register

app = create_app()
register(app)


@app.route('/')
def hello():
    "root page"
    return "AiSails API Server"


if __name__ == '__main__':
    app.run(debug=True, port=3000)
