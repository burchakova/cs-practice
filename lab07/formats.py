import json

def csv_to_records(text: str) -> list[dict]:
    lines = [line for line in text.strip().splitlines() if line.strip()]
    if not lines:
        return []
    header = [h.strip() for h in lines[0].split(",")]
    records = []
    for line in lines[1:]:
        values = [v.strip() for v in line.split(",")]
        records.append(dict(zip(header, values)))
    return records


def _parse_scalar(value: str):
    value = value.strip()
    lowered = value.lower()

    # 1. Булевы значения (как в задании)
    if lowered in ("true", "yes"):
        return True
    if lowered in ("false", "no"):
        return False

    # 2. Целые числа
    try:
        return int(value)
    except ValueError:
        pass

    # 3. Дробные числа (с точкой или запятой)
    # Если в строке есть запятая, пробуем заменить её на точку для float
    try:
        return float(value)
    except ValueError:
        # Пробуем с заменой запятой на точку
        try:
            return float(value.replace(",", "."))
        except ValueError:
            pass

    # 4. Всё остальное — строка
    return value


def parse_settings(lines: list[str]) -> dict:
    settings = {}
    current_list_key = None

    for raw in lines:
        # Отбрасываем всё после #
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        stripped = line.strip()

        # Элемент списка
        if stripped.startswith("- "):
            if current_list_key is not None:
                settings[current_list_key].append(_parse_scalar(stripped[2:]))
            continue

        if ":" not in stripped:
            continue

        # Ключ и значение
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()

        if not value:
            settings[key] = []
            current_list_key = key
        else:
            settings[key] = _parse_scalar(value)
            current_list_key = None

    return settings


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    result = []
    for row in rows:
        row_key = str(row.get(key, ""))
        addition = extra.get(row_key, {})
        merged = {**addition, **row}
        result.append(merged)
    return result


def records_to_json(records: list[dict]) -> str:
    return json.dumps(records, indent=2, sort_keys=True, ensure_ascii=False)
