// News image 22 Nov 2026 — entry program (Node 22, standard library only).
//
// The entry image is entry.png beside this file: a one-page summary of the
// world's news of Sunday 22 November 2026 (two hero stories, eight grid
// stories, twelve briefs, a markets ticker), drawn for this entry and
// approved by the entrant. This program copies it to /output/entry.png and
// verifies the copy byte for byte against the image's sha256, so a bad copy
// can never reach the judge. It runs twice and writes the same bytes both
// times: it reads only entry.png and writes only the one output file.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from 'node:crypto';
import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// sha256 of entry.png as built and approved, 22 Nov 2026.
const EXPECTED_SHA256 =
  '21d9024524e5789f5a8d20763b80fa784b6ce0eaeafb4dc7b6536c20afdcf375';

function sha256Hex(bytes: Buffer): string {
  return createHash('sha256').update(bytes).digest('hex');
}

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const source = join(here, 'entry.png');
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  const target = join(outDir, 'entry.png');

  const bytes = readFileSync(source);

  // The file must really be a PNG of the brief's 1024x1024: check the
  // 8-byte PNG signature, then the IHDR width/height (big-endian uint32
  // at bytes 16-20 and 20-24), before trusting the hash.
  const PNG_SIGNATURE = Buffer.from([
    0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
  ]);
  if (
    bytes.length < 24 ||
    !bytes.subarray(0, 8).equals(PNG_SIGNATURE) ||
    bytes.readUInt32BE(16) !== 1024 ||
    bytes.readUInt32BE(20) !== 1024
  ) {
    throw new Error(
      'entry.png is not a 1024x1024 PNG (bad signature or dimensions)',
    );
  }

  const digest = sha256Hex(bytes);
  if (digest !== EXPECTED_SHA256) {
    throw new Error(
      `entry.png sha256 mismatch: got ${digest}, expected ${EXPECTED_SHA256}`,
    );
  }

  mkdirSync(outDir, { recursive: true });
  copyFileSync(source, target);

  const written = readFileSync(target);
  if (sha256Hex(written) !== EXPECTED_SHA256) {
    throw new Error('written /output/entry.png failed its sha256 check');
  }
}

main();
