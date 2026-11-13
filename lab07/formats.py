"""Работа с тремя форматами данных: CSV, простой YAML и JSON."""

import json


def csv_to_records(text: str) -> list[dict]:
    """Разбирает CSV с заголовком в список словарей. Значения остаются строками."""
    records = []
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return records
    headers = [h.strip() for h in lines[0].split(",")]
    for line in lines[1:]:
        values = [v.strip() for v in line.split(",")]
        record = {}
        for i, header in enumerate(headers):
            record[header] = values[i] if i < len(values) else ""
        records.append(record)
    return records


def _parse_value(value: str):
    """Приводит строковое значение к числу, bool или оставляет строкой."""
    value = value.strip()
    low = value.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
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
    """Разбирает учебное подмножество YAML: пары «ключ: значение», списки, комментарии."""
    settings = {}
    current_list_key = None
    for line in lines:
        line = line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if current_list_key is not None and line.lstrip().startswith("- "):
            item = line.lstrip()[2:].strip()
            settings[current_list_key].append(_parse_value(item))
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value == "":
            settings[key] = []
            current_list_key = key
        else:
            settings[key] = _parse_value(value)
            current_list_key = None
    return settings


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    """Дополняет записи сведениями из справочника extra по значению ключа key."""
    merged = []
    for row in rows:
        record_key = row.get(key)
        extra_data = extra.get(record_key, {}) if record_key is not None else {}
        merged.append({**extra_data, **row})
    return merged


def records_to_json(records: list[dict]) -> str:
    """Список словарей в JSON: отступ 2, ключи по алфавиту, кириллица без экранирования."""
    return json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True)
