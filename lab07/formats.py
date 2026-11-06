"""Перевод данных между форматами: CSV, простой YAML, JSON."""

import json


def csv_to_records(text: str) -> list[dict]:
    """CSV с заголовком -> список словарей. Значения остаются строками."""
    records: list[dict] = []
    lines = text.strip().split("\n")
    if not lines or not lines[0].strip():
        return records
    headers = [h.strip() for h in lines[0].split(",")]
    for line in lines[1:]:
        if not line.strip():
            continue
        values = [v.strip() for v in line.split(",")]
        records.append(dict(zip(headers, values)))
    return records


def _parse_value(value: str):
    """Приводит строковое значение YAML к типу: число, истина/ложь или строка."""
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
    """Простой YAML -> словарь. Комментарии после # отбрасываются,
    списки открываются строкой 'ключ:' и заполняются строками '- значение'."""
    settings: dict = {}
    current_list: str | None = None

    for raw in lines:
        # всё после # — комментарий, отбрасываем
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        stripped = line.strip()

        # элемент списка
        if stripped.startswith("- ") and current_list is not None:
            settings[current_list].append(_parse_value(stripped[2:]))
            continue

        if ":" not in stripped:
            continue

        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()
        if value == "":
            # ключ без значения открывает список
            settings[key] = []
            current_list = key
        else:
            settings[key] = _parse_value(value)
            current_list = None

    return settings


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    """Дополняет записи сведениями из справочника extra по ключу key.
    Поля самой записи важнее: если ключ есть и там, и там, остаётся значение из записи."""
    merged: list[dict] = []
    for row in rows:
        record = dict(row)
        lookup = record.get(key)
        addition = extra.get(lookup)
        if addition is not None:
            # сначала справочник, потом запись — запись перекрывает
            record = {**addition, **record}
        merged.append(record)
    return merged


def records_to_json(records: list[dict]) -> str:
    """Список словарей -> JSON: отступ 2, ключи по алфавиту, кириллица как есть."""
    return json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True)

   
