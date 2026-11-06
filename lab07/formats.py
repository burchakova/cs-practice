import json

def csv_to_records(text: str) -> list[dict]:
    """CSV с заголовком → список словарей. Значения остаются строками."""
    lines = text.strip().splitlines()
    if not lines or not lines[0].strip():
        return []

    # Убираем пробелы вокруг заголовков
    header = [h.strip() for h in lines[0].split(",")]
    records = []
    
    for line in lines[1:]:
        if not line.strip():
            continue
        # Убираем пробелы вокруг самих значений
        values = [v.strip() for v in line.split(",")]
        records.append(dict(zip(header, values)))
        
    return records


def _parse_scalar(value: str):
    """Приводит строку к числу, иначе оставляет строкой."""
    value = value.strip()
    
    # Попытка распознать целое число
    try:
        return int(value)
    except ValueError:
        pass
        
    # Попытка распознать дробное число
    try:
        return float(value)
    except ValueError:
        pass
        
    # Если не число — возвращаем как есть (булевы оставляем строками)
    return value


def parse_settings(lines: list[str]) -> dict:
    """Простой YAML: «ключ: значение», списки через «- », комментарии после #."""
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

        # Разделяем ключ и значение
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()

        # Если значения нет — это начало списка
        if not value:
            settings[key] = []
            current_list_key = key
        else:
            settings[key] = _parse_scalar(value)
            current_list_key = None

    return settings


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    """Дополняет записи сведениями из словаря по значению ключа key."""
    result = []
    for row in rows:
        row_key = str(row.get(key, ""))
        addition = extra.get(row_key, {})
        # Поля самой записи важнее, поэтому row обновляет addition
        merged = {**addition, **row}
        result.append(merged)
    return result


def records_to_json(records: list[dict]) -> str:
    """Список словарей → JSON: отступ 2, ключи по алфавиту, кириллица как есть."""
    return json.dumps(records, indent=2, sort_keys=True, ensure_ascii=False)
