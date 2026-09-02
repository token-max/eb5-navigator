# EB-5 decision brief

A single-file, self-contained brief on an EB-5 rural set-aside filing: whether the petition
gets approved, and whether the capital comes back. No external requests, no analytics, no
build step, no framework.

## Contents

`index.html` is the decision brief. `projects.html` is a companion board comparing the ten
offering documents that were read for it. Both are single files. The brief itself is **encrypted at rest** — the file ships
only ciphertext plus a lock screen. Entering the passphrase derives an AES-256-GCM key with
PBKDF2-SHA256 (600,000 iterations) in the browser and decrypts the document in place. The
passphrase is never transmitted; a correct one is held in `sessionStorage` so a reload within
the same tab does not re-prompt.

Without the passphrase there is nothing readable in the source, in the repository, or to a
crawler.

## Reading levels

The decrypted brief has two, switchable in the header:

- **Explain it** — plain-language walkthrough for a first-time reader. Reference tables and
  operational checklists stay collapsed; a "Start here" section covers what EB-5 is, the
  seven-step journey, and the terminology.
- **Everything** — every table, checklist, quotation and source expanded.

## Re-encrypting after an edit

Edit the plaintext source, then regenerate `index.html` with the same passphrase. The
ciphertext, salt and IV are all embedded in the output file.
