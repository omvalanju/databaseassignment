from flask import Flask
from .config import Config
from app.routes.user import user_bp
from app.routes.run import run_bp
from app.routes.ecg import ecg_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(run_bp)
    app.register_blueprint(ecg_bp)

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000, debug=True)