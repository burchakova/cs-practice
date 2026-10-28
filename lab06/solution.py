from collections import Counter

def count_by_extension(paths: list[str]) -> dict[str, int]:
    def get_ext(name: str) -> str:
        if name.startswith(".") and name.count(".") == 1:
            return ""
        return name.rsplit(".", 1)[-1].lower() if "." in name else ""
    return dict(Counter(get_ext(p.split("/")[-1]) for p in paths))

def deepest_path(paths: list[str]) -> str:
    if not paths:
        return ""
    max_depth = max(p.count("/") for p in paths)
    candidates = [p for p in paths if p.count("/") == max_depth]
    return min(candidates, key=str.lower)

def human_size(n_bytes: int) -> str:
    units = ["Б", "КБ", "МБ", "ГБ", "ТБ"]
    i = 0
    size = float(n_bytes)
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
    return f"{int(size)} Б" if i == 0 else f"{size:.1f} {units[i]}"


    
   
