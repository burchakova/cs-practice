import sys
from logstats import count_levels, top_errors, format_report


def main():
    path = sys.stdin.readline().strip()
    if not path:
        return

    total_lines = 0
    error_count = 0
    broken_count = 0

    with open(path, encoding="utf-8") as log:
        for line in log:
            total_lines += 1
            line_stripped = line.rstrip("\n")
            if not line_stripped.strip():
                broken_count += 1
                continue

            parts = line_stripped.split(maxsplit=2)
            if len(parts) < 3:
                broken_count += 1
                continue

            _, level, _ = parts
            if level not in {"DEBUG", "INFO", "WARNING", "ERROR"}:
                broken_count += 1
                continue

            if level == "ERROR":
                error_count += 1

    print(total_lines)
    print(error_count)
    print(broken_count)

    with open(path, encoding="utf-8") as log:
        counts = count_levels(log)

    with open(path, encoding="utf-8") as log:
        errors = top_errors(log, 5)

    report = format_report(counts, errors)

    with open("report.txt", "w", encoding="utf-8") as out:
        out.write(report)


if __name__ == "__main__":
    main()
