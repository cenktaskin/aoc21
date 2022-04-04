import numpy as np

input_file = "input.txt"

fold_instructions_started = False
fold_instructions = []
dots = []
with open(input_file, 'r') as f:
    for line in f.readlines():
        line = line.replace("\n", "")
        if line == "":
            fold_instructions_started = True
            continue
        if not fold_instructions_started:
            dots.append(line.split(","))
        else:
            fold_instructions.append(line)

dots = np.array(dots, dtype=int)
paper = np.zeros(dots.max(axis=0, initial=0)[::-1] + 1, dtype=int)
for dot in dots:
    paper[dot[1], dot[0]] = 1


def fold_paper(paper, edge, axs):
    if axs == "y":
        return paper[:edge, :] + np.flip(paper[edge + 1:, :], axis=0)
    else:  # "x"
        return paper[:, :edge] + np.flip(paper[:, edge + 1:], axis=1)


# part 1
[axs, edge] = fold_instructions[0].split(" ")[-1].split("=")
part1_paper = fold_paper(paper, int(edge), axs)
print(part1_paper)
print(np.sum(part1_paper>0))
# part 2

for instruction in fold_instructions:
    [axs, edge] = instruction.split(" ")[-1].split("=")
    paper = fold_paper(paper, int(edge), axs)


np.set_printoptions(linewidth=100000)
paper[paper>1]=1
print(paper)
print(np.sum(paper>0))