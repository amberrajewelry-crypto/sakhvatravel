#!/usr/bin/env node
/**
 * Auto-sync /ru/ redirects in vercel.json
 * Scans all index.html files and ensures /ru/PATH -> /PATH redirect exists
 * Run before deploy: node scripts/sync-redirects.js
 */

const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');

const configPath = path.join(ROOT, 'vercel.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

// Collect all existing redirect sources
const existingSources = new Set(config.redirects.map(r => r.source));

// Scan all index.html pages
const skipDirs = new Set(['node_modules', '.git', '.vercel', 'api', '.agents', '.claude', 
  'scripts', 'data', 'research', 'schema', 'js', 'css', 'fonts', 'images',
  '.gstack', '.taskmaster', '.firecrawl', '.netlify', '.specify', 'test-results']);

function scanPages(dir, prefix = '') {
  const pages = [];
  for (const entry of fs.readdirSync(dir)) {
    if (skipDirs.has(entry)) continue;
    const full = path.join(dir, entry);
    if (fs.statSync(full).isDirectory()) {
      const indexPath = path.join(full, 'index.html');
      if (fs.existsSync(indexPath)) {
        const relPath = '/' + path.relative(ROOT, full).replace(/\\/g, '/') + '/';
        // Skip /en/ pages (they don't need /ru/ redirects)
        if (!relPath.startsWith('/en/')) {
          pages.push(relPath);
        }
      }
      pages.push(...scanPages(full, prefix));
    }
  }
  return pages;
}

const allPages = scanPages(ROOT);
let added = 0;

for (const pagePath of allPages) {
  const ruSource = '/ru' + pagePath;
  if (!existingSources.has(ruSource)) {
    // Find position: before wildcard /ru/ redirects
    let insertIdx = config.redirects.findIndex(r => r.source === '/ru/ekskursiya/:path*');
    if (insertIdx === -1) insertIdx = config.redirects.length;
    
    config.redirects.splice(insertIdx, 0, {
      source: ruSource,
      destination: pagePath,
      statusCode: 301
    });
    existingSources.add(ruSource);
    added++;
  }
}

if (added > 0) {
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  console.log(`sync-redirects: added ${added} new /ru/ redirects (total: ${config.redirects.length})`);
} else {
  console.log(`sync-redirects: all /ru/ redirects up to date (${config.redirects.length} total)`);
}
