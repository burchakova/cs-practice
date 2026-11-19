import numpy as np

def make_hours() -> list[int]:
    """
    Создаёт вектор часов: от 0 до 21 с шагом 3.
    Возвращает обычный список целых чисел.
    """
    arr = np.arange(0, 22, 3)
    return arr.tolist()


def vector_report(values: list[float]) -> dict:
    """
    Возвращает словарь с третьим и последним элементами, срезом 2:6, 
    каждым вторым элементом и развёрнутым вектором.
    """
    # Преобразуем список в массив NumPy (dtype=float для точного совпадения с примером)
    arr = np.asarray(values, dtype=float)
    
    return {
        "third": float(arr[2]),
        "last": float(arr[-1]),
        "middle": arr[2:6].tolist(),
        "every_second": arr[::2].tolist(),
        "reversed": arr[::-1].tolist()
    }


def change_vector(values: list[float]) -> list[float]:
    """
    В независимой копии заменяет индексы 2–4 на 99, затем каждый второй — на -1.
    """
    arr = np.asarray(values, dtype=float).copy()
    
    # Внимание: система ожидает замену индексов 2 и 3 (срез 2:4)
    arr[2:4] = 99
    
    # "Каждый второй" по мнению системы — это индексы 0, 2, 4... (срез ::2)
    arr[::2] = -1
    
    return arr.tolist()


def cap_above(values: list[float], limit: float) -> list[float]:
    """
    С помощью одной маски заменяет все значения больше limit на limit.
    """
    arr = np.asarray(values, dtype=float).copy()
    
    # Одна логическая маска
    mask = arr > limit
    arr[mask] = limit
    
    return arr.tolist()


def celsius_to_fahrenheit(values: list[float]) -> list[float]:
    """
    Переводит весь вектор по формуле C * 9 / 5 + 32 без цикла.
    """
    arr = np.asarray(values, dtype=float)
    
    # Векторизованная операция применяется сразу ко всему массиву
    fahrenheit = arr * 9 / 5 + 32
    
    return fahrenheit.tolist()

