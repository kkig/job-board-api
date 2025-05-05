from celery import shared_task
from django.core.mail import send_mail

# Celery Beat
from datetime import timedelta
from django.utils import timezone
from .models import Job


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
def mark_expired_jobs():
    print("Running mark_expired_jobs task")
    threshold_date = timezone.now() - timedelta(days=30)

    expired_jobs = Job.objects.filter(
        posted_at__lt=threshold_date,
        is_expired=False
        )
    count = expired_jobs.count()
    print(f"Found {count} expired jobs")

    if count > 0:
        updated_count = expired_jobs.update(is_expired=True)
        print(f"🧹 Deactivated {updated_count} expired job(s).")
    else:
        print("No jobs to mark as expired.")


@shared_task
def test_task():
    print("Test task run")
