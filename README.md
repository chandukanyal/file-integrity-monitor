# File Integrity Monitoring System

## Overview
A Python-based File Integrity Monitoring tool that
detects unauthorized file changes using SHA-256 hashes.

## Features
- SHA-256 file hashing
- Baseline creation
- Modified file detection
- Deleted file detection
- New file detection
- Automated integrity reports

## Technologies
- Python
- hashlib
- JSON
- pathlib

## How It Works
1. Create a baseline of monitored files.
2. Calculate file hashes.
3. Compare current hashes against baseline.
4. Detect file modifications, additions, and deletions.
5. Generate a security report.

## Disclaimer
Created for educational purposes and authorized
security monitoring.
