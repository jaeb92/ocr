import numpy as np

comp_list = [[[0, 30, -1], [22, 32, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 30, -1], [25, 34, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 30, 22], [3, 30, 16], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 30, 22], [6, 38, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 30, 22], [22, 44, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 34, -1], [23, 35, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 34, 3], [0, 43, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 34, 3], [22, 32, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 36, 22], [0, 50, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 36, 22], [3, 30, 16], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 36, 22], [6, 38, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 36, 22], [16, 50, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 36, 22], [17, 38, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 36, 22], [17, 43, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 36, 22], [20, 30, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 36, 22], [20, 34, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 36, 22], [22, 43, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 36, 22], [22, 50, 8], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 36, 22], [23, 43, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 36, 22], [29, 49, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 37, -1], [16, 36, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 38, -1], [8, 36, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 38, -1], [20, 50, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 38, 22], [23, 43, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 39, 22], [20, 50, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 39, 22], [22, 43, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 39, 22], [23, 43, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 43, -1], [16, 50, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 43, 0], [16, 50, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 43, 0], [23, 35, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 43, 3], [20, 30, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 43, 3], [23, 30, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 48, 0], [6, 38, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 48, 16], [0, 30, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 50, 16], [25, 34, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 50, 16], [28, 38, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[0, 50, 16], [29, 31, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[3, 30, 16], [17, 43, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[3, 38, 22], [29, 36, 17], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 30, 3], [0, 43, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 31, -1], [0, 36, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 31, -1], [0, 43, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 31, -1], [6, 34, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 31, -1], [6, 38, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 31, -1], [8, 50, 16], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 31, -1], [20, 50, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 31, -1], [22, 44, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 31, -1], [23, 34, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 31, -1], [23, 50, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 38, 22], [0, 30, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 38, 22], [0, 43, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 38, 22], [16, 36, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 38, 22], [20, 34, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 38, 22], [20, 50, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 38, 22], [22, 30, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 38, 22], [22, 32, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 38, 22], [22, 44, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 38, 22], [22, 49, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[6, 38, 22], [23, 43, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[8, 43, -1], [27, 34, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[16, 30, -1], [20, 30, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[16, 36, 22], [23, 50, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[16, 38, 0], [22, 44, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[16, 38, 0], [28, 38, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[16, 43, 3], [0, 36, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[17, 31, -1], [23, 31, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[17, 31, 0], [20, 34, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[17, 43, -1], [0, 36, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[17, 43, -1], [20, 30, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[17, 43, -1], [25, 34, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 30, 16], [22, 47, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 30, 22], [16, 36, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 30, 22], [23, 50, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 34, -1], [0, 30, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 34, -1], [0, 36, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 34, -1], [22, 36, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 34, -1], [22, 43, 8], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 34, -1], [22, 44, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 34, -1], [22, 50, 8], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 34, -1], [23, 34, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 34, 3], [8, 50, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 34, 3], [16, 43, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 34, 22], [0, 36, 8], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 34, 22], [22, 43, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 35, -1], [0, 36, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 35, -1], [16, 36, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 35, -1], [23, 38, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 35, -1], [29, 30, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 38, 22], [0, 38, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 38, 22], [22, 44, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 38, 22], [29, 38, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 43, -1], [20, 34, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 43, -1], [22, 44, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 43, 3], [25, 34, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 43, 22], [20, 50, 8], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 50, 3], [0, 36, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 50, 3], [0, 43, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 50, 3], [8, 30, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 50, 3], [20, 34, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 50, 3], [29, 30, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[20, 50, 3], [29, 48, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 30, -1], [23, 43, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 30, 3], [6, 38, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 30, 3], [20, 30, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 30, 3], [22, 32, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 36, -1], [23, 43, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 36, 3], [20, 34, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 36, 3], [20, 35, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 36, 3], [22, 30, 16], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 36, 22], [3, 30, 16], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 36, 22], [20, 30, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 37, -1], [20, 43, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 38, -1], [20, 30, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 42, 22], [22, 50, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 43, -1], [20, 34, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 43, -1], [20, 38, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 43, 8], [20, 30, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 44, 3], [0, 39, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 46, -1], [6, 34, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 47, -1], [22, 44, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 47, -1], [29, 30, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 48, 8], [23, 50, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 50, 3], [6, 34, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 50, 3], [23, 35, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 50, 3], [25, 34, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[22, 50, 3], [29, 30, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[23, 30, 22], [22, 30, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[23, 34, 3], [3, 30, 16], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[23, 34, 3], [17, 43, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[23, 34, 3], [23, 43, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[23, 35, -1], [23, 43, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[23, 38, -1], [20, 34, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[23, 43, 22], [17, 43, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[23, 43, 22], [22, 30, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[23, 43, 22], [22, 44, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[25, 30, 22], [20, 50, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[25, 30, 22], [22, 44, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[25, 34, 22], [22, 30, 16], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[25, 34, 22], [22, 43, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[25, 34, 22], [23, 43, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[25, 38, -1], [6, 30, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[25, 38, 22], [20, 50, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[25, 43, 22], [3, 30, 16], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[25, 43, 22], [17, 43, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[25, 43, 22], [25, 34, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[26, 30, 8], [17, 50, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[28, 36, 22], [27, 31, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[28, 38, -1], [29, 30, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 30, 3], [0, 36, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 30, 3], [3, 30, 16], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 30, 3], [6, 38, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 30, 3], [8, 30, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 30, 3], [8, 36, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 30, 3], [8, 50, 16], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 30, 3], [17, 30, 27], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 30, 3], [17, 43, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 30, 3], [20, 34, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 30, 3], [20, 34, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 30, 3], [20, 35, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 30, 3], [20, 50, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 30, 3], [22, 32, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 30, 3], [22, 36, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 36, 17], [20, 34, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 37, -1], [23, 34, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 38, -1], [3, 30, 16], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 38, -1], [20, 30, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 38, -1], [20, 34, -1], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 38, -1], [22, 44, 3], [6, 31, -1], [29, 30, 0], [0, 42, -1]], [[29, 38, 22], [22, 50, 0], [6, 31, -1], [29, 30, 0], [0, 42, -1]]]
target_list = [[[23, 43, 22], [22, 32, 22], [6, 31, -1], [29, 30, 0], [0, 42, -1]]]
def get_distance(*args):
    m = []
    for vin, v in enumerate(args[0]):
        for cin, comp in enumerate(args[1]):
            # print(len(v), len(comp))
            if len(v) == len(comp):
                m.append(np.sum(np.sqrt(np.subtract(v, comp) ** 2) / 2.0))
                # print(f'단어 간 거리계산: {np.sum(np.sqrt(np.subtract(v, comp) ** 2) / 2.0)}, index: {cin}')
                # print()
    min_index = np.argmin(m)
    # print(mi)
    return m, min_index


# m = get_distance(*comp_list, *target_list)
# print(f'm: {m}')