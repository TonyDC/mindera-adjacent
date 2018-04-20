import json
import argparse

ACTIVE_ELEMENT = 1


# (0, 0) -> top-left corner
# input_matrix = [[0, 0, 0, 1, 0, 0, 1, 1],
#                 [0, 0, 1, 1, 1, 0, 1, 1],
#                 [0, 0, 0, 0, 0, 0, 1, 0],
#                 [0, 0, 0, 1, 0, 0, 1, 1],
#                 [0, 0, 0, 1, 0, 0, 1, 1]]


def process_matrix(file, width: int) -> list:
    # a list containing the groups where the cells of the previous line belong to
    # the list is updated as the current row is processed
    previous_line_groups = [-1 for _ in range(width)]
    # the groups list
    groups = []
    current_height = 0

    for row in process_row_string(file):
        row_length = len(row)
        if row_length != width:
            raise ValueError(
                "the width of the matrix ({}) is not the same as the supplied one ({})".format(row_length, width))

        for i in range(width):
            if row[i] == ACTIVE_ELEMENT:
                previous_line_group = previous_line_groups[i]

                # if the first element in the row is connected to the above cell
                if i == 0 and previous_line_group > -1:
                    groups[previous_line_group].append([current_height, i])

                # remaining elements of the row
                elif i > 0:
                    previous_line_group_previous_element = previous_line_groups[i - 1]

                    # if different groups are connected, join them (consider the group with the lower rank)
                    if -1 < previous_line_group_previous_element != previous_line_group > -1:

                        # reassign previously defined group + add current point to group
                        if previous_line_group_previous_element < previous_line_group:
                            groups[previous_line_group_previous_element].extend(groups[previous_line_group])
                            groups.pop(previous_line_group)
                            previous_line_groups[i] = previous_line_groups[i - 1]

                        else:
                            groups[previous_line_group].extend(groups[previous_line_group_previous_element])
                            groups.pop(previous_line_group_previous_element)
                            previous_line_groups[i - 1] = previous_line_groups[i]

                        groups[previous_line_groups[i]].append([current_height, i])

                    # if the cell is connected to the previous cell
                    elif previous_line_group_previous_element > -1:
                        previous_line_groups[i] = previous_line_group_previous_element
                        groups[previous_line_group_previous_element].append([current_height, i])

                    # if the cell is connected to the above cell
                    elif previous_line_group > -1:
                        groups[previous_line_group].append([current_height, i])

                    # a new group is created
                    else:
                        groups.append([[current_height, i]])
                        previous_line_groups[i] = len(groups) - 1

            # remove group index
            else:
                previous_line_groups[i] = -1

        current_height += 1

    return groups


def print_groups(groups: list) -> None:
    for group in groups:
        if len(group) > 1:
            print(group)


def process_row_string(file) -> list:
    for line in file:
        row_string = line.strip()
        if row_string.endswith("],"):
            row_string = row_string[:-1]
        if len(row_string) > 1:
            yield json.loads(row_string)


# parse arguments: filename width
parser = argparse.ArgumentParser(description='Find adjacent cells in a 2D matrix')
parser.add_argument('filename', metavar='file', action='store', type=str, help='path to file containing the matrix')
parser.add_argument('width', metavar='width', type=int, action='store', help='the width of the matrix')

args = parser.parse_args()

try:
    with open(args.filename) as matrix_file:
        print_groups(process_matrix(matrix_file, args.width))
except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)
