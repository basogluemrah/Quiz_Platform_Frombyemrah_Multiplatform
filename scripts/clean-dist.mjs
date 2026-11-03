import { lstat, rm } from 'node:fs/promises';
import { resolve } from 'node:path';
const target = resolve('dist');
if (target !== resolve(process.cwd(), 'dist')) throw new Error('Unexpected build path');
try {
  if ((await lstat(target)).isSymbolicLink()) throw new Error('Build directory must not be a link');
  await rm(target, { recursive: true, force: true });
} catch (error) {
  if (error.code !== 'ENOENT') throw error;
}
