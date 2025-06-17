@echo off
echo [1/3] 🔄 makemigrations...
py ..\apps\backend_admin\manage.py makemigrations

echo [2/3] 🗃️ migrate...
py ..\apps\backend_admin\manage.py migrate

echo [3/3] 🧬 동기화 실행 중...
py sync_schema.py

pause