from celery.task.schedules import crontab
from celery.decorators import periodic_task


@periodic_task(run_every=(crontab()))
def some_task():
    # do something
    print('working')
    print('working pt2')