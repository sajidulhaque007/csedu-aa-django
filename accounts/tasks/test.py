from celery import shared_task


@shared_task(bind=True)
def test_task(self):
    return "Done"
