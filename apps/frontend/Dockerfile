# apps/frontend/Dockerfile

# 1단계: 종속성 설치 및 빌드
FROM node:22.15.0-alpine AS builder

# 작업 디렉토리 설정
WORKDIR /app

# frontend 디렉토리의 package 파일만 복사
COPY ./package.json ./package-lock.json ./
#COPY ./next.config.js ./
# 종속성 설치 (개발 의존성 포함)
RUN npm ci

# 전체 소스 복사 (이 Dockerfile이 apps/frontend 안에 있기 때문에 . 기준)
COPY . .

# Next.js 빌드
RUN npm run build
# 2단계: 실행 전용 경량 이미지
FROM node:22.15.0-alpine AS runner

# 작업 디렉토리 설정
WORKDIR /app

# NODE_ENV 설정
ENV NODE_ENV=production

# production 의존성만 설치
COPY ./package.json ./package-lock.json ./
RUN npm ci --omit=dev

# 빌드된 산출물 및 필요한 파일 복사
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.js ./
#COPY --from=builder /app/.env.production ./
COPY --from=builder /app/out ./
# Next.js 서버 포트
EXPOSE 3000

# 앱 실행 명령
CMD ["npx", "next", "start"]

