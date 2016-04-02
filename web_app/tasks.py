import celery
from flask import current_app

@celery.task
def update_counts_from_redis():
    return 0
