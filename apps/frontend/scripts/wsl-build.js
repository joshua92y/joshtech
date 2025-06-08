const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs-extra"); // npm install fs-extra

// 원본(윈도우) 경로 & 대상(WSL 홈) 경로
const SRC = "/mnt/c/code/AIX/joshtech/apps/frontend";
const DST = `${process.env.HOME}/frontend`;

console.log("📦 프로젝트 복사 중...");
fs.removeSync(DST);
fs.copySync(SRC, DST);

process.chdir(DST);
console.log("🧹 node_modules, .next, package-lock.json 삭제");
fs.removeSync("node_modules");
fs.removeSync(".next");
fs.removeSync("package-lock.json");

console.log("📦 npm install 시작");
execSync("npm install", { stdio: "inherit" });

console.log("⚡️ Cloudflare Next.js 빌드 실행");
execSync("npx @cloudflare/next-on-pages", { stdio: "inherit" });
