# joshtech

dev.info
#etc
conda deactivate # 가상환경 종료
conda remove --name admin-env --all # 가상환경 제거
pip install -r requirements.txt #설치 pip
pip freeze > requirements.txt #설치 pip 저장

#개발서버
uvicorn app.main:app --reload --port 8001 #8001번 포트 fastapi 서버런
python manage.py runserver # 8000번 포트 django 서버런
http://127.0.0.1:8001/docs #fastapi 관리페이지
http://127.0.0.1:8000/admin # django admin 페이지
http://127.0.0.1:8001/ # fastapi 페이지
http://127.0.0.1:8000/ # django 페이지

pytest tests/ #api 테스트

1. 아나콘다 개발 환경변수 셋팅
   conda init # 콘다초기화
   conda create -n admin-env python=3.11 #호완성 좋은 3.11 파이썬으로 셋팅
   conda activate admin-env #콘다런
   ->vs code 인터프린터 파이썬 가상환경으로 변경 Python: Select Interpreter → admin-env

2.Django
python manage.py startapp myapp #신규앱 생성
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser #슈퍼개정 생성
python manage.py dbshell
python manage.py flush #DB 초기화
3.FastAPI

4.sync-schema (django와 fastapi 스키마 연동을 위한 자동화 프로그램)
cd sync-schema # 자동화 프로그램 dir
./sync-schema.sh # 유닉스 계열
sync-schema.bat # 윈도우 더블클릭 or 실행

5.fly.io
flyctl machine run registry.fly.io/joshtech-api:latest --app joshtech-api # fly.io에서 최초 앱 만들고 실행하여 머신 셋팅
fly certs create joshtech-api.fly.dev -a joshtech-api #SSL 인증서 최초 발급
fly ips allocate-v4 --shared -a joshtech-api #공유 ip 할당
fly ips allocate-v6 #v6 할당
flyctl status -a joshtech-api #api 서버가동 여부확인
flyctl logs -a joshtech-api #api서버 로그 확인
https://joshtech-api.fly.dev/docs #Swagger UI

6.render
render 에서는 ssl 인증서 자동 발급
render logs --resources srv-d0ao2a1r0fns73co2n90 로그확인

7.next.js
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
npx create-next-app@latest frontend
npx npm-check-updates -u
npm uninstall @humanwhocodes/object-schema
npx shadcn@latest add button
npm install
npm run build
npm run lint
npm run dev
npx prettier --write .
npm run lint --fix

8.Chromium
choco install chromium --pre #power shell
C:\Program Files\Chromium\Application\chrome.exe 설치경로

9.OCI
cat ./id_rsa | clip
ssh -i .\id_rsa ubuntu@152.69.233.183 #fastapi
ssh -i .\id_rsa ubuntu@158.180.87.55 #cache
docker logs -f dragonfly
