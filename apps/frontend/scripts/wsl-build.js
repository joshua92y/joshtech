const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs-extra");

// 원본(윈도우) 경로 & 대상(WSL 홈) 경로
const SRC = "/mnt/c/Users/Admin/Desktop/portfolio/apps/frontend";
const DST = `${process.env.HOME}/frontend`;

// 복사에서 제외할 경로(폴더/파일)
const EXCLUDES = [
  "node_modules",
  ".next",
  ".git",
  "package-lock.json",
  ".DS_Store",
];

// 복사 필터 함수
function filterFunc(src, dest) {
  // src 경로의 마지막 요소(폴더명/파일명)
  const base = path.basename(src);
  // 제외 목록에 포함되어 있으면 false
  if (EXCLUDES.includes(base)) return false;
  return true;
}

console.log("📦 프로젝트 복사 중 (필요한 파일만)...");
fs.removeSync(DST);
fs.copySync(SRC, DST, { filter: filterFunc });

process.chdir(DST);
console.log("🧹 node_modules, .next, package-lock.json 삭제");
fs.removeSync("node_modules");
fs.removeSync(".next");
fs.removeSync("package-lock.json");

console.log("📦 npm install 시작");
execSync("npm install", { stdio: "inherit" });

console.log("⚡️ Cloudflare Next.js 빌드 실행");
execSync("npx @cloudflare/next-on-pages", { stdio: "inherit" });

console.log("🚀 Wrangler로 Cloudflare Pages 배포 실행!");
execSync(
  "wrangler pages deploy .vercel/output/static --project-name=joshtech-frontend --branch=main",
  { stdio: "inherit" }
);