import subprocess
import argparse
from datetime import datetime

def get_git_log(since_date, until_date):
    try:
        result = subprocess.run(
            ['git', 'log', '--since', since_date, '--until', until_date, '--pretty=format:%h | %an | %s | %ad', '--date=short'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
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
    parser = argparse.ArgumentParser(description="Generate Git reports for the current date by default.")
    parser.add_argument(
        '-d', '--date',
        help="Specify a date in YYYY-MM-DD format (default: today's date)",
        default=datetime.now().strftime('%Y-%m-%d')  # Default to today's date
    )
    parser.add_argument(
        '-o', '--output',
        help="Specify output file name (default: git_report.txt)",
        default='git_report.txt'
    )
    args = parser.parse_args()

    # Generate report for the given date
    since_date = args.date
    until_date = args.date
    print(f"Generating report for {since_date}...")
    
    git_log = get_git_log(since_date, until_date)
    if git_log.startswith("Error"):
        print(git_log)
    else:
        print(git_log)
        write_report(git_log, args.output)

if __name__ == "__main__":
    main()
