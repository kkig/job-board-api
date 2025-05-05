from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_application_notification(to_email, job_title, applicant_name):
    print(f"[CELERY TASK] Email to {to_email} about job: {job_title}")
    send_mail(
        subject=f"New Application for {job_title}",
        message=f"{applicant_name} has applied for your job: {job_title}.",
        from_email="no-reply@jobboard.com",
        recipient_list=[to_email],
    )


@shared_task
def test_task():
    print("Test task run")
