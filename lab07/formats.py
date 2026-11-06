import json
def csv_to_records(text: str) -> list[dict]:
    """CSV с заголовком -> список словарей. Значения остаются строками."""
    records = 
    # Убираем лишние пробелы по краям всего текста и разбиваем на строки
    lines = text.strip().split("\n")
    
    if not lines or not lines.strip():
        return records
    
    # Первая строка - заголовки. Обязательно делаем strip для каждого элемента!
    headers = [h.strip() for h in lines.split(",")]
    
    for line in lines[1:]:
        if not line.strip():
            continue
        # Разбиваем строку и сразу чистим пробелы у каждого значения
        values = [v.strip() for v in line.split(",")]
        records.append(dict(zip(headers, values)))
        
    return records


def _parse_value(value: str):
    """
    Приводит строковое значение к нужному типу.
    Порядок проверок важен: сначала булевы, потом числа, потом строка.
    """
    if not value:
        return value
        
    stripped = value.strip()
    low = stripped.lower()
    
    # 1. Сначала проверяем булевы значения (True/False, Yes/No)
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    
    # 2. Потом пробуем целое число
    try:
        return int(stripped)
    except ValueError:
        pass
    
    # 3. Потом дробное число (только если есть точка)
    # "3,5" не пройдет этот блок, так как там запятая, и останется строкой
    if "." in stripped:
        try:
            return float(stripped)
        except ValueError:
            pass
            
    # 4. Если ничего не подошло - возвращаем строку
    return stripped


def parse_settings(lines: list[str]) -> dict:
    """Простой YAML -> словарь."""
    settings = {}
    current_list_key = None
    
    for raw_line in lines:
        # Сначала убираем комментарий (#) и лишние пробелы справа
        line = raw_line.split("#", 1).rstrip()
        
        if not line.strip():
            continue
            
        stripped = line.strip()
        
        # Проверка на элемент списка: начинается с "- "
        if stripped.startswith("- ") and current_list_key is not None:
            # Берем текст после "- " и парсим его
            item_text = stripped[2:]
            settings[current_list_key].append(_parse_value(item_text))
            continue
        
        # Если это не список, ищем ключ: значение
        if ":" not in stripped:
            continue
            
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()
        
        if value == "":
            # Ключ без значения открывает список
            settings[key] = 
            current_list_key = key
        else:
            # Парсим значение (тут и сработает исправление для true/false)
            settings[key] = _parse_value(value)
            current_list_key = None
            
    return settings


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    """Объединяет записи, приоритет у полей из основной записи."""
    merged = 
    for row in rows:
        record = dict(row)
        lookup_id = row.get(key)
        addition = extra.get(lookup_id)
        
        if addition is not None:
            # Сначала добавляем данные из справочника, потом из записи (запись перезапишет дубликаты)
            record = {**addition, **record}
            
        merged.append(record)
    return merged


def records_to_json(records: list[dict]) -> str:
    """Список словарей -> JSON строка."""
    return json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True)
