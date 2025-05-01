# joshtech
dev.info
#etc
conda deactivate # 가상환경 종료
conda remove --name admin-env --all # 가상환경 제거

#개발서버
uvicorn app.main:app --reload --port 8001 #8001번 포트 fastapi 서버런
python manage.py runserver # 8000번 포트 django 서버런
http://127.0.0.1:8001/docs #fastapi 관리페이지
http://127.0.0.1:8000/admin # django admin 페이지
http://127.0.0.1:8001/ # fastapi 페이지
http://127.0.0.1:8000/ # django 페이지

1. 아나콘다 개발 환경변수 셋팅
conda create -n admin-env python=3.11 #호완성 좋은 3.11 파이썬으로 셋팅
conda activate admin-env #콘다런
conda install django # django install
conda install -c conda-forge fastapi uvicorn python-dotenv #fastapi install
conda install -c conda-forge datamodel-code-generator # datamodel-code-generator install

2.Django
3.FastAPI
4.sync-schema #  django와 fastapi 스키마 연동을 위한 자동화 프로그램
    cd sync-schema
    ./sync-schema.sh         # 유닉스 계열
    sync-schema.bat          # 윈도우 더블클릭 or 실행