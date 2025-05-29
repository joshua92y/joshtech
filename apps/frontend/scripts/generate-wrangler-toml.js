// generate-wrangler-toml.js
const fs = require("fs");
const path = require("path");

const compatibilityDate = new Date().toISOString().split("T")[0]; // YYYY-MM-DD

const tomlContent = `
name = "joshtech-frontend"
compatibility_date = "${compatibilityDate}"
pages_build_output_dir = ".vercel/output/static"
compatibility_flags = ["nodejs_compat"]
`.trim();

const targetPath = path.resolve(__dirname, "../wrangler.toml");

fs.writeFileSync(targetPath, tomlContent);
console.log(`✅ wrangler.toml generated at: ${targetPath}`);
