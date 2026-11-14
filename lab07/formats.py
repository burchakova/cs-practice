import json


# Разбирает CSV с заголовком в список словарей. Значения остаются строками.
def csv_to_records(text: str) -> list[dict]:
    result = []
    keys = []

    formated_text = text.strip().splitlines()

    if len(formated_text) == 0:
        return result

    for key in formated_text[0].split(","):
        keys.append(key.strip())

    for line in formated_text[1:]:
        fragment = {}

        for i, value in enumerate(line.split(",")):
            fragment[keys[i]] = value.strip()

        result.append(fragment)

    return result


# Простой YAML: «ключ: значение», списки через «- », комментарии после #.
def parse_settings(lines: list[str]) -> dict:
    result = {}
    current_key = None

    for line in lines:
        line = line.split("#", 1)[0].strip()

        if line == "":
            continue

        if line.startswith("- "):
            value = line[2:]

            match value:
                case "true" | "yes":
                    value = True
                case "false" | "no":
                    value = False
                case _:
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value.replace(',', '.'))
                        except ValueError:
                            if value.startswith('"') and value.endswith('"'):
                                value = value[1:-1]
                            elif value.startswith("'") and value.endswith("'"):
                                value = value[1:-1]

            result[current_key].append(value)
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value == "":
            result[key] = []
            current_key = key
            continue

        current_key = None

        match value:
            case "true" | "yes":
                value = True
            case "false" | "no":
                value = False
            case _:
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value.replace(',', '.'))
                    except ValueError:
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]

        result[key] = value

    return result


# Дополняет записи сведениями из словаря по значению ключа key.
def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    result = []

    for row in rows:
        fragment = {}

        if row[key] in extra:
            for name, value in extra[row[key]].items():
                fragment[name] = value

        for name, value in row.items():
            fragment[name] = value

        result.append(fragment)

    return result


# Список словарей в JSON: отступ 2, ключи по алфавиту, кириллица как есть.
def records_to_json(records: list[dict]) -> str:
    return json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True)
