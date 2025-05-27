@echo off
echo [1/3] 🔄 makemigrations...
..\apps\backend_admin\manage.py makemigrations

echo [2/3] 🗃️ migrate...
..\apps\backend_admin\manage.py migrate

echo [3/3] 🧬 동기화 실행 중...
sync_schema.py

pause