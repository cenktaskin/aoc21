#!/usr/bin/env python
import sys
import logging
import numpy as np


def parse_input(inp: str) -> dict[int, np.ndarray]:
    scan_data = {}
    report_blocks = [x.split("\n") for x in inp.split("\n\n")]
    for block in report_blocks:
        scanner_ind = int(block[0].split(" ")[2])
        logging.debug(f"Parser:New scanner is being read: {scanner_ind}")
        scan_data[scanner_ind] = np.array(
            [[int(i) for i in line.split(",")] for line in block[1:] if line != ""]
        )
        logging.debug(f"Parser:Read {len(scan_data[scanner_ind])} beacons.")
    logging.debug(
        f"Total beacons read: {sum([len(scan_data[sc]) for sc in scan_data])}"
    )
    return scan_data


def euclidean_distance(p0, p1):
    return np.sqrt(np.sum(np.square(p0 - p1), axis=-1))


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

    # TODO: change this part, doesn't look good
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
    transformation_dict = {i: {} for i in scan_data.keys()}
    for ind_scanner0 in scan_data:
        for ind_scanner1 in range(ind_scanner0 + 1, max(scan_data) + 1):
            h_mat = find_transformation_btw(scan_data, ind_scanner0, ind_scanner1)
            if h_mat is None:
                continue
            transformation_dict[ind_scanner0][ind_scanner1] = h_mat
            transformation_dict[ind_scanner1][ind_scanner0] = invert_h(h_mat)

    explored_dict = explore_transformations(transformation_dict)
    explored_dict[0][0] = np.eye(4)
    return explored_dict


def main():
    input_file = "input.txt"
    with open(f"day19/{input_file}", "r") as f:
        raw_input = f.read()

    scanners = parse_input(raw_input)

    transformation_dict = create_transformations_dict(scanners)

    points = []
    for ind in scanners:
        beaconsi_0 = transformation_dict[0][ind] @ make_points_homogenous(scanners[ind])
        points.append(beaconsi_0.T.astype(int))
    points = np.vstack(points)[:, :-1]
    print(f"Total scanned beacon count:{len(points)}")
    unique_points = np.unique(points, axis=0)
    print(f"Unique beacon count:{len(unique_points)}")
    # print(unique_points)

    # p0 = scanners[0]
    # p1 = scanners[1]
    # transformation = transformation_dict[0][1]
    # p1_0 = transformation @ make_points_homogenous(p1)
    # p1_0 = p1_0[:-1, :].T.astype(int)
    # print(p0)
    # print(p1_0)
    # set0 = set(tuple(x) for x in p0)
    # set1 = set(tuple(x) for x in p1_0)
    # commons = np.array([x for x in set0 & set1])
    # if len(commons) > 0:
    #     print(commons)
    #     commons_1 = invert_h(transformation_dict[0][1]) @ make_points_homogenous(
    #         commons
    #     )
    #     print(commons_1[:-1, :].T)


def parse_args(args: list) -> list:
    if "--debug" in args:
        logging.basicConfig(level=logging.DEBUG)
        args.remove("--debug")
    return args


if __name__ == "__main__":
    # The answer is 306
    parse_args(sys.argv)
    main()
