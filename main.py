import numpy as np
import pandas as pd

df = pd.read_csv("data.csv", delimiter=';')

matrix = np.zeros(36).reshape(6, 6)
clusters_list = ["1", "2", "3", "4", "5", "6"]

# Заполнение матрицы из CSV таблицы
for i in range(6):
    for j in range(6):
        if j == i:
            continue
        matrix[i, j] = np.round(np.sqrt(np.square(df['Sells'][i] - df['Sells'][j])
                                        + np.square(df['Avg'][i] - df['Avg'][j])), 2)

# Нахождение индексов минимального числа в матрице
def find_min():
    min, row, column = np.max(matrix), 0, 0
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if j <= i:
                continue
            if matrix[i, j] < min:
                min = matrix[i, j]
                row = i
                column = j
    return np.array([row, column])

# Функция кластеризации
def clusterize(n, m):
    size = len(matrix) - 1
    temp_matrix = np.zeros(np.square(size)).reshape(size, size)

    k, l = 0, 0
    for i in range(size + 1):
        for j in range(size + 1):
            if i >= j:
                l += 1
                continue
            if i == m:
                i += 1
                continue
            if j == m:
                j += 1
                continue
            if j == n:
                temp_matrix[k, l] = np.min([matrix[i, n], matrix[i, m]])
            if i == n:
                temp_matrix[k, l] = np.min([matrix[j, n], matrix[j, m]])
            else:
                temp_matrix[k, l] = matrix[i, j]
            l += 1
        l = 0
        k += 1

    for i in range(size):
        for j in range(size):
            temp_matrix[j, i] = temp_matrix[i, j]

    print(temp_matrix, '\n')
    return temp_matrix


print(matrix, '\n')

while len(matrix) > 2:
    row, column = find_min()[0], find_min()[1]
    clusters_list[row] += clusters_list[column]
    del clusters_list[column]
    matrix = clusterize(row, column)

print("Минимальное расстояние:", matrix[0, 1])
print("Кластеры:", sorted(clusters_list[0]), "и", sorted(clusters_list[1]))
