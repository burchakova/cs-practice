from collections import Counter

def count_by_extension(paths: list[str]) -> dict[str, int]:
    exts = [p.rsplit(".", 1)[-1].lower() if "." in p else "" for p in paths]
    return dict(Counter(exts))


def deepest_path(paths: list[str]) -> str:
    if not paths:
        return ""
    return min((p for p in paths if p.count("/") == max(p.count("/") for p in paths)), key=str.lower)


def human_size(n_bytes: int) -> str:
    units = ["Б", "КБ", "МБ", "ГБ", "ТБ"]
    i = 0
    size = n_bytes
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
    return f"{size:.1f} {units[i]}" if i > 0 else f"{int(size)} Б"


    
   
