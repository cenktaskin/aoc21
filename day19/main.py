#!/usr/bin/env python
import sys
import logging
import numpy as np


def parse_args(args: list) -> list:
    if "--debug" in args:
        logging.basicConfig(level=logging.DEBUG)
        args.remove("--debug")
    return args


def parse_input(inp: list[str]) -> list[np.ndarray]:
    scanner_list, beacon_list, scanner_name = [], [], None
    for line in inp:
        if line[:3] == "---":
            scanner_name = "".join(line.split(" ")[1:-1])
            logging.debug(f"Parser:New scanner is being read: {scanner_name}")
            continue
        elif line == "":
            logging.debug(
                f"Parser:Scanner reading is done. Total {len(beacon_list)} beacons"
            )
            scanner_list.append(np.array(beacon_list))
            beacon_list = []
        else:
            beacon_list.append(np.array([int(i) for i in line.split(",")]))
            logging.debug(f"Parser:Beacon at {beacon_list[-1]} added to {scanner_name}")
    return scanner_list


def euclidean_distance(p0, p1):
    return np.sqrt(np.sum(np.square(p0.copy() - p1.copy()), axis=-1))


def invert_h(h):
    r = h[:-1, :-1]
    t = h[:-1, -1]
    h_inv = np.zeros((4, 4), dtype=int)
    h_inv[-1, -1] = 1
    h_inv[:-1, :-1] = r.T
    h_inv[:-1, -1] = -r.T @ t
    return h_inv


def create_distance_matrix(scan_data):
    dst_mat = np.zeros((len(scan_data), len(scan_data)))
    for i, p in enumerate(scan_data):
        dst_mat[i, i:] = euclidean_distance(p, scan_data[i:])
    return dst_mat


def pad_cols_if_necessary(dst0, dst1):
    if (n_cols0 := dst0.shape[1]) != (n_cols1 := dst1.shape[1]):
        target = max(n_cols0, n_cols1)
        dst0 = np.pad(dst0, ((0, 0), (0, target - n_cols0)))
        dst1 = np.pad(dst1, ((0, 0), (0, target - n_cols1)))
    return dst0, dst1


def map_common_points(dst0, dst1):
    dst0, dst1 = pad_cols_if_necessary(dst0, dst1)
    all_dst = np.vstack([dst0, dst1])
    vals, idxs, cnts = np.unique(all_dst, return_index=True, return_counts=True)
    vals, idxs = vals[cnts == 2], idxs[cnts == 2]

    # 12 beacons will have 66 overlaping distances, C(12,2)=66
    if len(vals) < 66:
        return None, None

    map_mat = np.zeros((len(dst0), len(dst1)))
    for i in range(len(vals)):
        idx0 = idxs[i] // dst0.shape[1], idxs[i] % dst0.shape[1]
        idx1 = map(int, np.where(dst1 == vals[i]))
        for ind in [(x, y) for y in idx1 for x in idx0]:
            map_mat[ind] += 1
    ind_src, ind_dst = np.where(map_mat > 1)
    return ind_src, ind_dst


def make_points_homogenous(p):
    return np.hstack([p, np.ones((len(p), 1))]).T


def solve_for_h(p0, p1):
    src = make_points_homogenous(p0)
    dst = make_points_homogenous(p1)
    inv = dst.T @ np.linalg.inv(dst @ dst.T)
    res = np.round(src @ inv).astype(int)
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


def print_dict_of_dict(d):
    for key in d:
        if len(d[key].keys()) >= 1:
            print(f"{key}->{list(d[key].keys())}")


def deduct_transformations(scanners):
    transformation_dict = {i: {} for i in range(len(scanners))}
    for ind_scanner0 in range(len(scanners)):
        for ind_scanner1 in range(ind_scanner0 + 1, len(scanners)):
            h_mat = find_transformation_btw(scanners, ind_scanner0, ind_scanner1)
            if h_mat is not None:
                transformation_dict[ind_scanner0][ind_scanner1] = h_mat
                transformation_dict[ind_scanner1][ind_scanner0] = invert_h(h_mat)


def explore_transformations(h_dict):
    if len(h_dict) - 1 == len(h_dict[0]):
        logging.debug("Explorer:Populated the dict enough.")
        return h_dict
    for interm in list(h_dict[0].keys()):
        for dst in h_dict[interm].keys():
            if dst not in h_dict[0].keys() and dst != 0:
                logging.debug(f"Explorer:New link 0->({interm})->{dst}")
                h_dict[0][dst] = h_dict[0][interm] @ h_dict[interm][dst]
    logging.debug("Explorer:Recurring")
    return explore_transformations(h_dict)


def create_transformations_dict(scan_data):
    transformation_dict = {i: {} for i in range(len(scan_data))}
    for ind_scanner0 in range(len(scan_data)):
        for ind_scanner1 in range(ind_scanner0 + 1, len(scan_data)):
            h_mat = find_transformation_btw(scan_data, ind_scanner0, ind_scanner1)
            if h_mat is not None:
                transformation_dict[ind_scanner0][ind_scanner1] = h_mat
                transformation_dict[ind_scanner1][ind_scanner0] = invert_h(h_mat)

    explored_dict = explore_transformations(transformation_dict)
    explored_dict[0][0] = np.eye(4)
    return explored_dict


def main():
    input_file = "input.txt"
    with open(f"day19/{input_file}", "r") as f:
        raw_input = f.read().splitlines()

    scanners = parse_input(raw_input)

    transformation_dict = create_transformations_dict(scanners)

    points = []
    for i, sca in enumerate(scanners):
        beacons_wrt0 = transformation_dict[0][i] @ make_points_homogenous(sca)
        points.append(beacons_wrt0.T.astype(int))
    points = np.vstack(points)[:, :-1]
    print(f"Total scanned beacon count:{len(points)}")
    unique_points = np.unique(points, axis=0)
    print(f"Unique beacon count:{len(unique_points)}")
    # print(unique_points)


if __name__ == "__main__":
    parse_args(sys.argv)
    main()
