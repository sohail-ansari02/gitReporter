import subprocess
import argparse
from datetime import datetime

def get_git_log(since, until):
    try:
        # Debugging: print the command to be executed
        command = [
            'git', 'log',
            '--since', since,
            '--until', until,
            '--pretty=format:%h | %an | %s | %ad',
            '--date=short'
        ]
        print(f"Executing: {' '.join(command)}")
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Debugging: Print stdout and stderr
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        if result.returncode != 0:
            raise Exception(result.stderr.strip())
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def write_report(report, output_file):
    try:
        with open(output_file, 'w') as file:
            file.write(report)
        print(f"Report saved to {output_file}")
    except Exception as e:
        print(f"Failed to save the report: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Generate Git reports for a specific date and time range.")
    parser.add_argument(
        '-d', '--date',
        help="Specify a date in YYYY-MM-DD format (default: today's date)",
        default=datetime.now().strftime('%Y-%m-%d')  # Default to today's date
    )
    parser.add_argument(
        '--start-time',
        help="Specify start time in HH:MM format (default: 00:00)",
        default="00:00"
    )
    parser.add_argument(
        '--end-time',
        help="Specify end time in HH:MM format (default: 23:59)",
        default="23:59"
    )
    parser.add_argument(
        '-o', '--output',
        help="Specify output file name (default: git_report.txt)",
        default='git_report.txt'
    )
    args = parser.parse_args()

    # Combine date with time to form the full datetime range
    since = f"{args.date} {args.start_time}"
    until = f"{args.date} {args.end_time}"

    print(f"Generating report from {since} to {until}...")

    git_log = get_git_log(since, until)
    if git_log.startswith("Error"):
        print(git_log)
    elif not git_log:
        print("No commits found for the given date and time range.")
    else:
        print("Git log fetched successfully.")
        print(git_log)
        write_report(git_log, args.output)

if __name__ == "__main__":
    main()
