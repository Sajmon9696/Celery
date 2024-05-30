from flask import Flask
from celery import Celery, Task
from flask_sqlalchemy import SQLAlchemy

from models import db


def make_celery(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with self.app.app_context():
                return self.run(*args, **kwargs)
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY']['broker_url'],
        backend=app.config['CELERY']['result_backend'],
        include=['tasks']
    )
    celery.conf.update(app.config['CELERY'])
    celery.Task = FlaskTask
    celery.Task.app = app  # Bind the Flask app to the task class
    return celery

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:///example.db',
        CELERY=dict(
            broker_url="redis://localhost:6379/0",
            result_backend="redis://localhost:6379/0",
            task_ignore_result=True,
        ),
    )
    app.config.from_prefixed_env()

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize Celery
    celery = make_celery(app)
    celery.set_default()



    return app, celery

flask_app, celery_app = create_app()
flask_app.app_context().push()

if __name__ == "__main__":
    flask_app.run(debug=True)
