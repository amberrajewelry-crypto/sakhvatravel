#!/usr/bin/env node
// Optimize all images in /images/ folder
// - Convert large JPGs to WebP (quality 80, max width 1200)
// - Re-compress existing WebP files that are >100KB
// - Skip MP4, PNG favicons, already-small files
// - Back up originals to /images/backup/

import sharp from 'sharp';
import { readdirSync, mkdirSync, statSync, copyFileSync } from 'fs';
import { join, extname, basename } from 'path';

const IMAGES_DIR = join(import.meta.dirname, '..', 'images');
const BACKUP_DIR = join(IMAGES_DIR, 'backup');
const MAX_WIDTH = 1200;
const WEBP_QUALITY = 80;
const SKIP_THRESHOLD = 50 * 1024; // skip files under 50KB

mkdirSync(BACKUP_DIR, { recursive: true });

const files = readdirSync(IMAGES_DIR).filter(f => {
  const ext = extname(f).toLowerCase();
  return ['.jpg', '.jpeg', '.webp', '.png'].includes(ext);
});

let totalSaved = 0;

for (const file of files) {
  const filePath = join(IMAGES_DIR, file);
  const stat = statSync(filePath);
  const ext = extname(file).toLowerCase();
  const name = basename(file, ext);

  // Skip small files
  if (stat.size < SKIP_THRESHOLD) {
    console.log(`  SKIP ${file} (${(stat.size / 1024).toFixed(0)} KB < 50 KB)`);
    continue;
  }

  // Skip favicons and logos
  if (file.includes('favicon') || file.includes('apple-touch')) {
    console.log(`  SKIP ${file} (favicon/icon)`);
    continue;
  }

  // Backup original
  copyFileSync(filePath, join(BACKUP_DIR, file));

  const outPath = join(IMAGES_DIR, name + '.webp');

  try {
    const img = sharp(filePath);
    const meta = await img.metadata();

    let pipeline = sharp(filePath);

    // Resize if wider than MAX_WIDTH
    if (meta.width > MAX_WIDTH) {
      pipeline = pipeline.resize(MAX_WIDTH, null, { withoutEnlargement: true });
    }

    // Convert to WebP
    await pipeline
      .webp({ quality: WEBP_QUALITY, effort: 6 })
      .toFile(outPath + '.tmp');

    // Replace original webp or create new
    const { size: newSize } = statSync(outPath + '.tmp');
    const saved = stat.size - newSize;
    totalSaved += saved;

    // Rename tmp to final
    const { renameSync, unlinkSync } = await import('fs');
    renameSync(outPath + '.tmp', outPath);

    // Remove original JPG if we created WebP
    if (ext === '.jpg' || ext === '.jpeg') {
      // Keep the JPG in backup, but check if site references it
      console.log(`  OK ${file} → ${name}.webp: ${(stat.size / 1024).toFixed(0)} KB → ${(newSize / 1024).toFixed(0)} KB (saved ${(saved / 1024).toFixed(0)} KB)`);
    } else {
      console.log(`  OK ${file}: ${(stat.size / 1024).toFixed(0)} KB → ${(newSize / 1024).toFixed(0)} KB (saved ${(saved / 1024).toFixed(0)} KB)`);
    }
  } catch (err) {
    console.error(`  ERR ${file}: ${err.message}`);
  }
}

console.log(`\nTotal saved: ${(totalSaved / 1024 / 1024).toFixed(1)} MB`);
