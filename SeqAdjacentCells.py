import json

ACTIVE_ELEMENT = 1


# (0, 0) -> top-left corner
# input_matrix = [[0, 0, 0, 1, 0, 0, 1, 1],
#                 [0, 0, 1, 1, 1, 0, 1, 1],
#                 [0, 0, 0, 0, 0, 0, 1, 0],
#                 [0, 0, 0, 1, 0, 0, 1, 1],
#                 [0, 0, 0, 1, 0, 0, 1, 1]]


def process_matrix(matrix: list, width: int) -> list:
    previous_line_groups = [-1 for _ in range(width)]
    groups = []
    current_height = 0

    while len(matrix) > 0:
        row = matrix.pop(0)

        for i in range(width):
            if row[i] == ACTIVE_ELEMENT:
                previous_line_group = previous_line_groups[i]

                if i == 0 and previous_line_group > -1:
                    groups[previous_line_group].append([current_height, i])

                elif i > 0:
                    previous_line_group_previous_element = previous_line_groups[i - 1]

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

                    elif previous_line_group_previous_element > -1:
                        previous_line_groups[i] = previous_line_group_previous_element
                        groups[previous_line_group_previous_element].append([current_height, i])

                    elif previous_line_group > -1:
                        groups[previous_line_group].append([current_height, i])

                    else:
                        groups.append([[current_height, i]])
                        previous_line_groups[i] = len(groups) - 1

            else:
                previous_line_groups[i] = -1

        current_height += 1

    return groups


input_matrix = json.load(open('matrices/10000x10000.json'))
matrix_width = len(input_matrix[0])

result = process_matrix(input_matrix, matrix_width)
# for group in result:
#    print(group)
