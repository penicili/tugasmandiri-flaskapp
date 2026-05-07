import logging
import traceback
import dotenv
from flask import Flask, jsonify
from app.db import init_db

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    dotenv.load_dotenv()
    app = Flask(__name__)

    init_db()

    from app.routes import bp
    app.register_blueprint(bp)

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error("Unhandled exception: %s\n%s", e, traceback.format_exc())
        return jsonify({'error': str(e)}), 500

    return app
