import json
import logging
from datetime import datetime

from flask import Flask, jsonify
from flask_caching import Cache
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
ma = Marshmallow()
cache = Cache(config={'CACHE_TYPE': 'simple'})


class JsonFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super(JsonFormatter, self).formatException(exc_info)
        json_result = {
            "timestamp": f"{datetime.now()}",
            "level": "ERROR",
            "logger": "app",
            "message": f"{result}",
        }
        return json.dumps(json_result)


json_formatter = JsonFormatter(
    '{"timestamp":"%(asctime)s", "level":"%(levelname)s", "logger":"%(module)s", "message":"%(message)s"}'
)


def create_app(config_name=None):
    app = Flask(__name__, )
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    CORS(app)

    logger = logging.StreamHandler()
    logger.setFormatter(json_formatter)
    logging.basicConfig(level=logging.INFO, handlers=[logger])
    app.logger.addHandler(logger)

    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)

    from app.stocks.views import stock_bp
    app.register_blueprint(stock_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({'code': 404, 'message': str(error)}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'code': 400, 'message': str(error)}), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'code': 500, 'message': 'Internal Error Server'}), 500

    return app
