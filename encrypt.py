#!/usr/bin/env -S uv run --quiet --with cryptography python3
"""Rebuild a page from a plaintext source, encrypted with a passphrase.

    ./encrypt.py <source.html> <passphrase> [output.html]

Writes the output next to this script (default `index.html`): a lock screen plus AES-256-GCM
ciphertext, with the key derived by PBKDF2-SHA256 over 600,000 iterations. The salt and IV are
generated fresh on every run, so re-encrypting the same text twice gives different output — that
is intended.
"""
import base64, hashlib, io, os, pathlib, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ITER = 600_000
HERE = pathlib.Path(__file__).resolve().parent

if len(sys.argv) not in (3, 4):
    sys.exit(__doc__)
src, pw = pathlib.Path(sys.argv[1]), sys.argv[2]
dest = HERE / (sys.argv[3] if len(sys.argv) == 4 else 'index.html')

plain = src.read_text(encoding='utf-8')
head = '<meta name="color-scheme" content="light dark">'
if head in plain and 'name="robots"' not in plain:
    plain = plain.replace(head,
        '<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">\n'
        '<meta name="referrer" content="no-referrer">\n' + head, 1)

salt, iv = os.urandom(16), os.urandom(12)
key = hashlib.pbkdf2_hmac('sha256', pw.encode(), salt, ITER, 32)
ct  = AESGCM(key).encrypt(iv, plain.encode('utf-8'), None)
b64 = lambda b: base64.b64encode(b).decode()

shell = (HERE / 'lock-template.html').read_text(encoding='utf-8')
out = (shell.replace('__SALT__', b64(salt))
            .replace('__IV__',   b64(iv))
            .replace('__CT__',   b64(ct))
            .replace('__ITER__', str(ITER)))
(dest).write_text(out, encoding='utf-8')
print(f'{dest.name}  {len(out):,} bytes  ({len(plain):,} bytes plaintext)')
