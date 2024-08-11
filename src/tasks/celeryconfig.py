from celery import Celery
from celery.schedules import crontab


app = Celery(
    "terehov_test_task",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

app.conf.beat_schedule = {
    "fetch_currency_rates": {
        "task": "src.tasks.fetch_currency_rates",
        "schedule": crontab(hour='6', minute='0'),
    },
}

app.conf.timezone = "Europe/Moscow"
