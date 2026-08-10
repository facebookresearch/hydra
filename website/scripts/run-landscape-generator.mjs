#!/usr/bin/env node

// Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const generator = fileURLToPath(
  new URL('../../tools/landscape/build_public_landscape.py', import.meta.url),
);
const forwardedArguments = process.argv.slice(2);
const configuredPython = process.env.PYTHON;
const candidates = configuredPython
  ? [[configuredPython, []]]
  : process.platform === 'win32'
    ? [
        ['py', ['-3']],
        ['python3', []],
        ['python', []],
      ]
    : [
        ['python3', []],
        ['python', []],
      ];

for (const [command, prefixArguments] of candidates) {
  const completed = spawnSync(
    command,
    [...prefixArguments, generator, ...forwardedArguments],
    {stdio: 'inherit'},
  );
  if (completed.error?.code === 'ENOENT') {
    continue;
  }
  if (completed.error) {
    console.error(`Failed to run ${command}: ${completed.error.message}`);
    process.exit(1);
  }
  process.exit(completed.status ?? 1);
}

console.error('Python 3 was not found. Set PYTHON to a Python 3 executable.');
process.exit(1);
