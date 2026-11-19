import numpy as np

hours = np.arange(0, 22, 3)
line = np.linspace(0, 1, 5)
zeros = np.zeros(6)
unknown_table = np.full((2, 3), -1)
identity = np.ones((3, 3))

print(f"""
{hours}
{hours.shape}
{hours.ndim}
{hours.size}
{hours.dtype}
""")

print(f"""
{hours[2]}
{hours[-1]}
{hours[2:5]}
{hours[::2]}
{hours[::-1]}
""")


temperatures = np.array(
    [
        [12, 14, 13, 15],
        [11, 13, 16, 17],
        [10, 12, 15, 18],
    ]
)

print(f"""
{temperatures.shape}
{temperatures.dtype}
{temperatures.size}
{temperatures[1][2]}
{temperatures[0]}
{temperatures.transpose()[-1]}
{temperatures[0:2, 1:]}
{temperatures[0:2, 1:-1]}
""")


matrix = np.arange(1, 26).reshape(5, 5)

print(f"""
{matrix[:3]}
{np.shape(matrix[:3])}
{matrix[-2:]}
{np.shape(matrix[-2:])}
{matrix[:,:2]}
{np.shape(matrix[:,:2])}
{matrix[1:3, 2:4]}
{np.shape(matrix[1:3, 2:4])}
{matrix[3:, 3:]}
{np.shape(matrix[3:, 3:])}
""")

# Создается новый объект в памяти.
changed_hours = hours.copy()

changed_hours[2:4] = 99
changed_hours[::2] = -1
print(f"""
{changed_hours}
{hours}
""")


changed_matrix = matrix.copy()

changed_matrix[2] = 0
changed_matrix[:, -1] = -1
changed_matrix[1:4, 1:4] = 100
print(f"""
{changed_matrix}
{matrix}
""")


numbers = np.arange(12)

table = numbers.reshape(3, 4)

transposed = table.T

print(f"""
{np.shape(numbers)}
{np.shape(table)}
{np.shape(transposed)}
""")
