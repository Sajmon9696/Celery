from celery import shared_task

from app import celery_app, db
from models import User
import random
import string

@shared_task
def add_users_async(n):
    for _ in range(n):
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        email = f"{username}@example.com"
        user = User(username=username, email=email)
        db.session.add(user)
    db.session.commit()
    return f"Added {n} users to the database."