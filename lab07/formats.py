import json

def csv_to_records(text: str) -> list[dict]:
    records = 
    lines = text.strip().split("\n")
    if not lines or not lines.strip():
        return records
    
    headers = [h.strip() for h in lines.split(",")]
    
    for line in lines[1:]:
        if not line.strip():
            continue
        values = [v.strip() for v in line.split(",")]
        # Важно: zip остановится на минимальной длине, если вдруг колонок не хватает
        records.append(dict(zip(headers, values)))
        
    return records


def _parse_value(value: str):
    value = value.strip()
    if not value:
        return value

    low = value.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False

    try:
        return int(value)
    except ValueError:
        pass

    # ГЛАВНОЕ ИСПРАВЛЕНИЕ: float только если есть точка. 
    # "3,5" не пройдет эту проверку и останется строкой.
    if "." in value:
        try:
            return float(value)
        except ValueError:
            pass

    return value


def parse_settings(lines: list[str]) -> dict:
    settings = {}
    current_list = None

    for raw in lines:
        # Сначала убираем комментарий (#)
        line = raw.split("#", 1).rstrip()
        if not line.strip():
            continue
        
        stripped = line.strip()

        # Обработка списка (- элемент)
        if stripped.startswith("- ") and current_list is not None:
            settings[current_list].append(_parse_value(stripped[2:]))
            continue

        if ":" not in stripped:
            continue

        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()

        if value == "":
            # Открываем список
            settings[key] = 
            current_list = key
        else:
            settings[key] = _parse_value(value)
            current_list = None

    return settings


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    merged = 
    for row in rows:
        record = dict(row)
        lookup_id = record.get(key)
        addition = extra.get(lookup_id)
        
        if addition is not None:
            # Справочник + Запись. Запись (справа) перекрывает справочник
            record = {**addition, **record}
            
        merged.append(record)
    return merged


def records_to_json(records: list[dict]) -> str:
    return json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True)





      
