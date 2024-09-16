from flask import Flask
from config import Config
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure UPLOAD_FOLDER is an absolute path
    app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.join(app.root_path, '..', 'uploads'))

    print(f"UPLOAD_FOLDER: {app.config['UPLOAD_FOLDER']}")
    print(f"UPLOAD_FOLDER exists: {os.path.exists(app.config['UPLOAD_FOLDER'])}")
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        print(f"Created UPLOAD_FOLDER: {app.config['UPLOAD_FOLDER']}")

    print(f"Static folder: {app.static_folder}")
    print(f"Static URL path: {app.static_url_path}")

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///classifications.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)

    from app import routes
    app.register_blueprint(routes.bp)

    return app