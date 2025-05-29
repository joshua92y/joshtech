// generate-wrangler-toml.js
const fs = require("fs");
const path = require("path");

const compatibilityDate = new Date().toISOString().split("T")[0]; // YYYY-MM-DD

const tomlContent = `
name = "joshtech-frontend"
compatibility_date = "${compatibilityDate}"

[build]
command = "npx @cloudflare/next-on-pages"

[build.environment]
NODE_VERSION = "20"

[[deployments]]
environment = "production"
`.trim();

const targetPath = path.resolve(__dirname, "../wrangler.toml");

fs.writeFileSync(targetPath, tomlContent);
console.log(`✅ wrangler.toml generated at: ${targetPath}`);
