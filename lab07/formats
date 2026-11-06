# formats.py

import json


def _to_typed_value(value_str: str):
    """Преобразует строку в подходящий тип: int, float, bool или str."""
    s = value_str.strip()
    if not s:
        return s

    # Проверка на целое число
    if s.isdigit() or (s.startswith('-') and s[1:].isdigit()):
        return int(s)

    # Проверка на float
    try:
        f = float(s)
        return f
    except ValueError:
        pass

    lower = s.lower()
    if lower in ("true", "yes"):
        return True
    if lower in ("false", "no"):
        return False

    return s


def csv_to_records(text: str) -> list[dict]:
    """
    CSV с заголовком → список словарей. Значения остаются строками.
    Разделитель — запятая, кавычек и запятых внутри значений нет.
    """
    lines = text.strip().splitlines()
    if not lines:
        return []

    headers = lines[0].split(',')
    records = []

    for line in lines[1:]:
        if not line.strip():
            continue
        values = line.split(',')
        # По условию количество полей совпадает с количеством заголовков
        record = {headers[i]: values[i] for i in range(len(headers))}
        records.append(record)

    return records


def parse_settings(lines: list[str]) -> dict:
    """
    Простой YAML (учебное подмножество) → словарь с приведением типов.
    Поддерживаются: ключ: значение, списки через '- ', комментарии после #.
    Вложенность не поддерживается.
    """
    result = {}
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # Удаляем комментарий
        if '#' in line:
            line = line[:line.index('#')]

        line_stripped = line.strip()
        if not line_stripped:
            i += 1
            continue

        if ':' in line_stripped:
            key_part, _, rest = line_stripped.partition(':')
            key = key_part.strip()
            rest = rest.strip()

            if rest:
                # Пара ключ: значение
                result[key] = _to_typed_value(rest)
                i += 1
                continue
            else:
                # Ключ без значения — начало списка
                items = []
                i += 1
                while i < n:
                    next_line = lines[i]
                    if '#' in next_line:
                        next_line = next_line[:next_line.index('#')]
                    next_stripped = next_line.strip()
                    if next_stripped.startswith('- '):
                        item_value = next_stripped[2:].strip()
                        items.append(_to_typed_value(item_value))
                        i += 1
                    else:
                        break
                result[key] = items
                continue

        i += 1

    return result


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    """
    Дополняет записи сведениями из словаря extra по значению ключа key.
    Поля самой записи имеют приоритет (не перезаписываются).
    Записи без пары в extra остаются без изменений.
    """
    merged = []
    for row in rows:
        new_row = dict(row)  # копия, чтобы не менять оригинал
        lookup_key = row.get(key)
        if lookup_key is not None and lookup_key in extra:
            extra_data = extra[lookup_key]
            for k, v in extra_data.items():
                if k not in new_row:
                    new_row[k] = v
        merged.append(new_row)
    return merged


def records_to_json(records: list[dict]) -> str:
    """
    Список словарей → JSON-строка.
    - Ключи в каждом объекте отсортированы по алфавиту.
    - Отступ — 2 пробела.
    - Кириллица не экранируется.
    """
    return json.dumps(
        records,
        sort_keys=True,
        indent=2,
        ensure_ascii=False
    )
