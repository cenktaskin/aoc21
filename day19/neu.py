#!/usr/bin/env python
import sys
import logging
import numpy as np


def parse_args(args: list) -> list:
    if "--debug" in args:
        logging.basicConfig(level=logging.DEBUG)
        args.remove("--debug")
    return args


def parse_input(inp):
    scanner_list = []
    beacon_list = []
    scanner_name = None
    for line in inp:
        if line[:3] == "---" and line[-3:] == "---":
            scanner_name = "".join(line.split(" ")[1:-1])
            logging.debug(f"New scanner is being read: {scanner_name}")
            continue
        elif line == "":
            logging.debug(f"Scanner reading is done. Total {len(beacon_list)} beacons")
            scanner_list.append(np.array(beacon_list))
            beacon_list = []
        else:
            coord = np.array([float(i) for i in line.split(",")])  # is float necessary
            beacon_list.append(coord)
            logging.debug(f"Beacon at {coord} added to {scanner_name}")
    return scanner_list


def euclidean_distance(p0, p1):
    return np.sqrt(np.sum(np.square(p0.copy() - p1.copy()), axis=-1))


def create_distance_matrix(scan_data):
    dst_mat = np.zeros((len(scan_data), len(scan_data)))
    for i, p in enumerate(scan_data):
        dst_mat[i, i:] = euclidean_distance(p, scan_data[i:])
    return dst_mat


def pad_columns_like(mat0, mat1):
    col0 = mat0.shape[1]
    col1 = mat1.shape[1]
    if col0 < col1:
        mat0 = np.hstack([mat0, np.zeros((col0, mat1.shape[0] - mat0.shape[0]))])
    else:
        mat1 = np.hstack([mat1, np.zeros((col1, mat0.shape[0] - mat1.shape[0]))])
    return mat0, mat1


def map_common_points(dst0, dst1):
    if (dim0 := dst0.shape[0]) != (dim1 := dst1.shape[0]):
        if dim0 < dim1:
            dst0 = np.hstack([dst0, np.zeros((dim0, dst1.shape[0] - dst0.shape[0]))])
        else:
            dst1 = np.hstack([dst1, np.zeros((dim1, dst0.shape[0] - dst1.shape[0]))])

    a = np.vstack([dst0, dst1])
    values, indexes, counts = np.unique(a, return_index=True, return_counts=True)
    values, indexes = values[counts == 2], indexes[counts == 2]

    # print(f"Common dist count:{len(values)}")
    # 12 beacons will have 66 overlaping distances, C(12,2)=66
    if len(values) < 66:
        # print("They don't overlap")
        return None, None

    map_mat = np.zeros((len(dst0), len(dst1)))
    for i in range(len(values)):
        common_d = values[i]
        idx0 = indexes[i] // dst0.shape[1], indexes[i] % dst0.shape[1]
        idx1 = map(int, np.where(dst1 == common_d))
        for ind in [(x, y) for y in idx1 for x in idx0]:
            map_mat[ind] += 1
    ind_src, ind_dst = np.where(map_mat > 1)
    # print(f"{ind_src} maps to {ind_dst}")
    return ind_src, ind_dst


def solve_for_h(p0, p1):
    src = np.hstack([p0, np.ones((len(p0), 1))]).T
    dst = np.hstack([p1, np.ones((len(p1), 1))]).T
    # print(src)
    # print(dst)
    inv = dst.T @ np.linalg.inv(dst @ dst.T)
    res = src @ inv
    res = np.round(res).astype(int)
    # print("Resulting transformation")
    # print(res)
    # print(res @ dst)
    return res


def find_transformation_btw(data, ind0, ind1):
    dst_mat0 = create_distance_matrix(data[ind0])
    dst_mat1 = create_distance_matrix(data[ind1])
    ind_src, ind_dst = map_common_points(dst_mat0, dst_mat1)
    if ind_src is not None:
        h_mat = solve_for_h(data[ind0][ind_src], data[ind1][ind_dst])
        return h_mat
    else:
        return None


def find_transformation_path(mat, src, dst, been=[]):
    print(f"Trying to reach to {src}->{dst}")
    been.append(src)
    leads = list(np.where(mat[src])[0])
    if dst in leads:
        print("reached")
        return
    if leads:
        for i in leads:
            if i not in been:
                find_transformation_path(mat, i, dst, been)


def main():
    input_file = "test-input.txt"
    with open(f"day19/{input_file}", "r") as f:
        raw_input = f.read().splitlines()

    # print(raw_input)
    scanners = parse_input(raw_input)
    all_vals = []
    for sca in scanners:
        dst_mat = list(create_distance_matrix(sca).flatten())
        all_vals += dst_mat
    all_vals = np.array(all_vals)
    v, c = np.unique(all_vals, return_counts=True)
    v = v[v > 0]
    print(v)
    print(len(v))
    print(c)
    # we could probably only solve it by checking the distances


if __name__ == "__main__":
    parse_args(sys.argv)
    main()
