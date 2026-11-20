import hashlib
import json
from pathlib import Path
from datetime import datetime

# Project paths
MONITORED_DIR = Path("monitored_files")
BASELINE_FILE = Path("baseline.json")
REPORT_FILE = Path("integrity_report.txt")


def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def get_file_hashes():
    """Collect hashes of files in the monitored directory."""
    file_hashes = {}

    for file_path in MONITORED_DIR.rglob("*"):
        if file_path.is_file():
            relative_path = str(file_path.relative_to(MONITORED_DIR))
            file_hashes[relative_path] = calculate_hash(file_path)

    return file_hashes


def create_baseline():
    """Create initial trusted file baseline."""
    hashes = get_file_hashes()

    with open(BASELINE_FILE, "w", encoding="utf-8") as file:
        json.dump(hashes, file, indent=4)

    print("\nBaseline created successfully!")
    print(f"Files monitored: {len(hashes)}")


def check_integrity():
    """Compare current files against the baseline."""

    if not BASELINE_FILE.exists():
        print("Baseline not found! Create a baseline first.")
        return

    with open(BASELINE_FILE, "r", encoding="utf-8") as file:
        baseline = json.load(file)

    current = get_file_hashes()

    modified = []
    deleted = []
    new_files = []

    # Detect modified and deleted files
    for file_name, old_hash in baseline.items():

        if file_name not in current:
            deleted.append(file_name)

        elif current[file_name] != old_hash:
            modified.append(file_name)

    # Detect new files
    for file_name in current:

        if file_name not in baseline:
            new_files.append(file_name)

    # Generate report
    report = []

    report.append("FILE INTEGRITY MONITOR REPORT")
    report.append("=" * 45)
    report.append(f"Date: {datetime.now()}")
    report.append("")

    report.append("MODIFIED FILES")
    report.append("-" * 45)

    report.extend(modified if modified else ["None"])

    report.append("")
    report.append("DELETED FILES")
    report.append("-" * 45)

    report.extend(deleted if deleted else ["None"])

    report.append("")
    report.append("NEW FILES")
    report.append("-" * 45)

    report.extend(new_files if new_files else ["None"])

    report.append("")
    report.append("=" * 45)

    if not modified and not deleted and not new_files:
        report.append("STATUS: No changes detected.")
    else:
        report.append("STATUS: Changes detected!")

    # Display report
    print("\n".join(report))

    # Save report
    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(report))

    print(f"\nReport saved to {REPORT_FILE}")


def main():
    MONITORED_DIR.mkdir(exist_ok=True)

    print("\nFILE INTEGRITY MONITOR")
    print("=" * 30)
    print("1. Create baseline")
    print("2. Check file integrity")
    print("3. Exit")

    choice = input("\nSelect an option: ")

    if choice == "1":
        create_baseline()

    elif choice == "2":
        check_integrity()

    elif choice == "3":
        print("Exiting program.")

    else:
        print("Invalid option!")


if __name__ == "__main__":
    main()