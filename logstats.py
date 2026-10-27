from collections import Counter
from typing import List, Dict, Any

VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR"}


def parse_event(line: str) -> Dict[str, Any]:
    line = line.strip()
    if not line:
        raise ValueError("Empty line")

    parts = line.split(maxsplit=2)
    if len(parts) < 3:
        raise ValueError("Not enough parts")

    time_str, level, message = parts

    if level not in VALID_LEVELS:
        raise ValueError(f"Unknown level: {level}")

    return {
        "time": time_str,
        "level": level,
        "message": message,
    }


def count_levels(lines: List[str]) -> Dict[str, int]:
    counts: Dict[str, int] = {}

    for line in lines:
        line_no_nl = line.rstrip("\n")
        if not line_no_nl.strip():
            counts["BROKEN"] = counts.get("BROKEN", 0) + 1
            continue

        try:
            event = parse_event(line_no_nl)
            level = event["level"]
            counts[level] = counts.get(level, 0) + 1
        except ValueError:
            counts["BROKEN"] = counts.get("BROKEN", 0) + 1

    for lvl in VALID_LEVELS:
        if lvl not in counts:
            counts[lvl] = 0

    return counts


def top_errors(lines: List[str], n: int) -> List[List[Any]]:
    error_messages = []

    for line in lines:
        line_no_nl = line.rstrip("\n")
        if not line_no_nl.strip():
            continue

        try:
            event = parse_event(line_no_nl)
            if event["level"] == "ERROR":
                error_messages.append(event["message"])
        except ValueError:
            pass

    counter = Counter(error_messages)
    sorted_items = sorted(counter.items(), key=lambda x: (-x[1], x[0]))

    result = [[msg, cnt] for msg, cnt in sorted_items[:n]]
    return result


def format_report(counts: Dict[str, int], errors: List[List[Any]]) -> str:
    levels_order = ["BROKEN"] + sorted([lvl for lvl in VALID_LEVELS])

    lines_out = ["Отчёт по журналу"]
    for lvl in levels_order:
        count = counts.get(lvl, 0)
        lines_out.append(f"{lvl}: {count}")

    lines_out.append("Частые ошибки:")
    for msg, cnt in errors:
        lines_out.append(f"- {msg} — {cnt}")

    report_text = "\n".join(lines_out) + "\n"
    return report_text
