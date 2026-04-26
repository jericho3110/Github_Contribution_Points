# 🌱 goGreen 

A Python version of the original project for creating backdated Git commits that show up on GitHub on past dates.

## About

This repository now uses Python to write a JSON file and create commits with backdated author and committer timestamps. These commits can appear on older dates in your GitHub contribution graph when pushed.

> Use this responsibly. Backdated commits are best for personal testing, experiment repositories, or learning Git behavior.

## Requirements

- Python 3.8 or newer
- `git` installed and available on your PATH
- A Git repository with a remote configured

## Usage

1. Clone the repository and enter the folder:

```bash
git clone https://github.com/fenrir2608/goGreen.git
cd goGreen
```

2. Run the Python script:

```bash
python go_green.py --count 100
```

This will create 100 backdated commits across the past year and push them to the current branch.

3. Create a single commit for a specific date:

```bash
python go_green.py --date 2025-05-17
```

## Options

- `--count`: Number of random past-date commits to create (default: 100)
- `--date`: Create one commit for the exact ISO date provided
- `--path`: Path to the JSON file updated before each commit (default: `data.json`)
- `--dry-run`: Print the dates that would be used without modifying Git

## Notes

- GitHub contribution graph uses commit timestamps and branch visibility.
- Commits must be pushed to a branch that GitHub counts as contributions (usually the default branch).
- The repo remains compatible with Python and uses the standard library only.

## Requirements

- No external Python packages are required.
- The script uses only built-in modules.
