from app import flask_app
from tasks import add_users_async

if __name__ == "__main__":
    with flask_app.app_context():
        result = add_users_async.delay(100)
        print("Task to add 100 users has been triggered.")
        print(f"Task ID: {result.id}")
