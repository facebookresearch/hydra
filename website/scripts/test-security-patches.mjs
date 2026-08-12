import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {mkdtempSync, rmSync, writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';

import {imageSize} from 'image-size';
import {imageSizeFromFile} from 'image-size/fromFile';

const cases = {
  heif() {
    const box = (name, payload, size = payload.length + 8) => {
      const result = Buffer.alloc(payload.length + 8);
      result.writeUInt32BE(size, 0);
      result.write(name, 4);
      payload.copy(result, 8);
      return result;
    };
    const ispePayload = Buffer.alloc(12);
    ispePayload.writeUInt32BE(1, 4);
    ispePayload.writeUInt32BE(1, 8);
    const ispe = box('ispe', ispePayload, 0);
    const ipco = box('ipco', ispe);
    const iprp = box('iprp', ipco);
    const meta = box('meta', Buffer.concat([Buffer.alloc(4), iprp]));
    const ftyp = box('ftyp', Buffer.from('avif'));
    return Buffer.concat([ftyp, meta]);
  },
  icns() {
    const input = Buffer.alloc(16);
    input.write('icns', 0);
    input.writeUInt32BE(input.length, 4);
    input.write('ICON', 8);
    input.writeUInt32BE(0, 12);
    return input;
  },
  jxl() {
    const box = (name, payload, size = payload.length + 8) => {
      const result = Buffer.alloc(payload.length + 8);
      result.writeUInt32BE(size, 0);
      result.write(name, 4);
      payload.copy(result, 8);
      return result;
    };
    const signature = box('JXL ', Buffer.alloc(4));
    const ftyp = box('ftyp', Buffer.from('jxl '));
    const jxlp = box('jxlp', Buffer.alloc(4), 0);
    return Buffer.concat([signature, ftyp, jxlp]);
  },
};

const childMarker = '--security-patch-child';
if (process.argv[2] === childMarker) {
  const [, , , api, format, filePath] = process.argv;
  try {
    if (api === 'buffer') {
      imageSize(cases[format]());
    } else {
      await imageSizeFromFile(filePath);
    }
  } catch {
    // Malformed files may throw; the security invariant is that parsing ends.
  }
  process.exit(0);
}

const temporaryDirectory = mkdtempSync(join(tmpdir(), 'hydra-image-size-'));
try {
  for (const [format, createInput] of Object.entries(cases)) {
    const filePath = join(temporaryDirectory, format);
    writeFileSync(filePath, createInput());
    for (const api of ['buffer', 'file']) {
      const result = spawnSync(
        process.execPath,
        [fileURLToPath(import.meta.url), childMarker, api, format, filePath],
        {encoding: 'utf8', timeout: 2000},
      );
      assert.equal(
        result.error?.code,
        undefined,
        `${api} ${format} parser did not terminate`,
      );
      assert.equal(
        result.status,
        0,
        result.stderr || `${api} ${format} parser failed unexpectedly`,
      );
    }
  }
} finally {
  rmSync(temporaryDirectory, {force: true, recursive: true});
}

console.log('Verified image-size malformed-image parsers terminate.');
