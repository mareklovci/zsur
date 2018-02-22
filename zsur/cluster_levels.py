import numpy as np
import datetime as dt


def distanc(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def generate_matrix(data):
    size = len(data)
    matrix = np.zeros((size, size), dtype=np.float)
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            matrix[j, i] = distanc(data[i], data[j])
            matrix[i, j] = matrix[j, i]
    return matrix
    # for i in np.nditer(matrix, op_flags=['readwrite']):


def matrix_min(matrix):
    minimum = np.min(matrix[np.nonzero(matrix)])
    index1, index2 = np.where(matrix == minimum)
    if len(index1) >= 2:
        return minimum, index2[0], index2[1]
    else:
        return minimum, index1[0], index2[0]


def reduce_matrix(matrix, row, column):
    for i in range(len(matrix)):
        if matrix[row, i] > matrix[column, i]:
            # matrix[row][i] = matrix[column][i]
            matrix[i, row] = matrix[i, column]
        else:
            # matrix[column][i] = matrix[row][i]
            matrix[i, column] = matrix[i, row]
    matrix = np.delete(matrix, column, 1)
    matrix = np.delete(matrix, column, 0)
    return matrix


def cluster_levels(data, boundary):
    t0 = dt.datetime.now()
    matrix = generate_matrix(data)
    t1 = dt.datetime.now()
    print('Matrix generated in {}'.format(t1 - t0))
    minimums = []
    t0 = dt.datetime.now()
    for i in range(len(matrix) - 1):
        minimums.append(matrix_min(matrix))
        matrix = reduce_matrix(matrix, minimums[i][1], minimums[i][2])
        t1 = dt.datetime.now()
        print('\rMatrix dimension: {}, time elapsed: {}'.format(len(matrix), t1 - t0), end='')
    classes = 0
    for i in range(len(minimums)):
        rev = list(reversed(minimums))
        if rev[i][0] / boundary >= rev[i + 1][0]:  # 1.9 magic constant
            classes += 1
        else:
            break
    print('\nAglomerativni metodou byly nalezeny: {} tridy'.format(classes))


def main():
    from main import readfile
    data = readfile('../data.txt')
    # data = [(-3, 1), (1, 1), (-2, 0), (3, -3), (1, 2), (-2, -1)]
    cluster_levels(data, 1.9)


if __name__ == '__main__':
    main()