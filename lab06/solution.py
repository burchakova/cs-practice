
from typing import List, Dict

def count_by_extension(paths: List[str]) -> Dict[str, int]:
    result = {}
    for path in paths:
        # берём имя файла: часть после последнего '/'
        filename = path.split('/')[-1]
        
        # ищем последнюю точку
        dot_index = filename.rfind('.')
        if dot_index == -1 or dot_index == len(filename) - 1:
            # нет точки или точка в конце (файл заканчивается на точку)
            ext = ""
        else:
            ext = filename[dot_index + 1:].lower()
        
        result[ext] = result.get(ext, 0) + 1
    return result


def deepest_path(paths: List[str]) -> str:
    if not paths:
        return ""
    
    # считаем вложенность по количеству '/'
    def nesting(path: str) -> int:
        return path.count('/')
    
    max_nest = -1
    candidates = []
    
    for p in paths:
        n = nesting(p)
        if n > max_nest:
            max_nest = n
            candidates = [p]
        elif n == max_nest:
            candidates.append(p)
    
    # при равенстве — первый по алфавиту
    return min(candidates)


def human_size(n_bytes: int) -> str:
    units = ["Б", "КБ", "МБ", "ГБ", "ТБ"]
    size = n_bytes
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        # байты — целое число
        return f"{int(size)} {units[unit_index]}"
    else:
        # остальные — один знак после запятой
        return f"{size:.1f} {units[unit_index]}"
