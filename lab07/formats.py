"""Работа с форматами данных: CSV, JSON, учебный YAML."""

import json


def csv_to_records(text: str) -> list[dict]:
    """CSV с заголовком → список словарей. Значения остаются строками."""
    lines = [line for line in text.strip().splitlines() if line.strip()]
    if not lines:
        return []

    header = lines[0].split(",")
    records = []
    for line in lines[1:]:
        values = line.split(",")
        records.append(dict(zip(header, values)))
    return records


def _parse_scalar(value: str):
    """Приводит строку к числу/булеву/строке по правилам учебного YAML."""
    value = value.strip()
    lowered = value.lower()

    if lowered in ("true", "yes"):
        return True
    if lowered in ("false", "no"):
        return False

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value


def parse_settings(lines: list[str]) -> dict:
    """Простой YAML: «ключ: значение», списки через «- », комментарии после #."""
    settings: dict = {}
    current_list_key = None

    for raw in lines:
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        stripped = line.strip()

        if stripped.startswith("- "):
            if current_list_key is not None:
                settings[current_list_key].append(_parse_scalar(stripped[2:]))
            continue

        if ":" not in stripped:
            continue

        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()

        if value == "":
            settings[key] = []
            current_list_key = key
        else:
            settings[key] = _parse_scalar(value)
            current_list_key = None

    return settings


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    """Дополняет записи сведениями из справочника extra по значению ключа key.

    Поля самой записи важнее: при совпадении остаётся значение из записи.
    """
    result = []
    for row in rows:
        row_key = str(row.get(key, ""))
        addition = extra.get(row_key, {})
        merged = {**addition, **row}
        result.append(merged)
    return result


def records_to_json(records: list[dict]) -> str:
    """Список словарей → JSON: отступ 2, ключи по алфавиту, кириллица как есть."""
    return json.dumps(records, indent=2, sort_keys=True, ensure_ascii=False)


      
