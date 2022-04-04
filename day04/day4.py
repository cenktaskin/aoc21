import numpy as np

input_file = "input.txt"
boards = np.loadtxt(input_file, skiprows=2, dtype=int).reshape((-1, 5, 5))
draws = np.loadtxt(input_file, delimiter=",", max_rows=1, dtype=int)
# part1
print(f"Bingo game starting...\nBoard count:{boards.shape[0]}")


def check_winner(b_results, last_b_results, part=1):
    if get_win_condition(b_results, part):
        if part == 1:
            win_board = np.where(b_results)[0][0]
        else:
            win_board = np.where(last_b_results == 0)[0][0]
        return True, win_board
    print("No winner yet!")
    return False, None


def get_win_condition(b_result, part):
    if part == 1:
        return np.any(b_result)
    else:
        return np.all(b_result > 0)


part = 2
current = np.zeros_like(boards)
last_board_result = None
for draw in draws:
    draw_result = (boards == draw).astype(int)
    current += draw_result
    print(f"{draw=}\nThere are {np.sum(draw_result)} hits")
    cols = (np.sum(current, axis=1) == 5).astype(int)
    rows = (np.sum(current, axis=2) == 5).astype(int)
    board_results = np.sum(cols + rows, axis=1)
    win_flag, winning_board = check_winner(board_results, last_board_result, part=part)
    if win_flag:
        sum_of_winner = np.sum((1 - current[winning_board]) * boards[winning_board])
        print(f"{winning_board=}")
        print(f"**There is a winner!**\nScore {sum_of_winner * draw}")
        break
    else:
        last_board_result = board_results
