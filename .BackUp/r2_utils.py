# apps\backend_admin\R2_Storage\r2_utils.py
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import now
from .models import FileMeta
import boto3, os


def clean_deleted_files():
    files = FileMeta.objects.filter(is_deleted=True).exclude(deleted_at__isnull=True)

    for f in files:
        try:
            s3.delete_object(Bucket=os.getenv("R2_BUCKET"), Key=f.key)
            f.delete()
        except Exception as e:
            print(f"R2 삭제 실패: {e}")


scheduler = BackgroundScheduler()
scheduler.add_job(clean_deleted_files, "interval", minutes=10)
scheduler.start()
