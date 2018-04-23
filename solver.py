import json


# (0, 0) -> top-left corner
# input_matrix = [[0, 0, 0, 1, 0, 0, 1, 1],
#                 [0, 0, 1, 1, 1, 0, 1, 1],
#                 [0, 0, 0, 0, 0, 0, 1, 0],
#                 [0, 0, 0, 1, 0, 0, 1, 1],
#                 [0, 0, 0, 1, 0, 0, 1, 1]]

class Solver:
    ACTIVE_ELEMENT = 1

    def __init__(self, filename):
        self.__matrix_width = -1
        self.__previous_line_groups = []
        self.__groups = []
        self.__nr_created_groups = 0
        self.__current_height = 0
        self.__is_matrix_processed = False
        self.__filename = filename
        self.__equivalent_groups = []

    def __process_matrix(self) -> None:
        for row in self.__process_row_string():
            row_length = len(row)

            if self.__matrix_width < 0:
                self.__matrix_width = row_length
                self.__previous_line_groups = [-1 for _ in range(row_length)]

            elif row_length != self.__matrix_width:
                raise ValueError("the width of the matrix ({}) is not uniform".format(self.__matrix_width))

            for i in range(self.__matrix_width):
                if row[i] == self.ACTIVE_ELEMENT:
                    self.__process_active_element(i)

                # this cell does not belong to any group
                else:
                    self.__previous_line_groups[i] = -1

            self.__current_height += 1

        self.__is_matrix_processed = True

    def __update_indices(self, old_index, new_index) -> None:
        if self.__equivalent_groups[old_index] != new_index:
            self.__equivalent_groups[old_index] = new_index
            self.__update_indices(old_index, self.__equivalent_groups[new_index])

    def __add_cell_to_group(self, group_id, row, column) -> None:
        self.__groups[group_id].append([row, column])

    def __process_active_element(self, i) -> None:
        previous_line_group = self.__previous_line_groups[i]

        # Update group ID if necessary (e.g. a merge was performed)
        if -1 < previous_line_group != self.__equivalent_groups[previous_line_group]:
            # Check whether the current group update was changed in the meanwhile
            self.__update_indices(previous_line_group,
                                  self.__equivalent_groups[self.__equivalent_groups[previous_line_group]])
            previous_line_group = self.__previous_line_groups[i] = self.__equivalent_groups[previous_line_group]

        # if the first element in the row is connected to the above cell
        if i == 0 and previous_line_group > -1:
            self.__add_cell_to_group(previous_line_group, self.__current_height, i)

        # remaining elements of the row
        elif i > 0:
            previous_line_group_previous_element = self.__previous_line_groups[i - 1]

            # if different groups are connected, join them (consider the group with the lower rank)
            if -1 < previous_line_group_previous_element != previous_line_group > -1:

                # reassign previously defined group + add current point to group
                if previous_line_group_previous_element < previous_line_group:
                    self.__reassign_groups(previous_line_group, previous_line_group_previous_element, i)

                else:
                    self.__reassign_groups(previous_line_group_previous_element, previous_line_group, i - 1)

                self.__add_cell_to_group(self.__previous_line_groups[i], self.__current_height, i)

            # if the cell is connected to the previous cell
            elif previous_line_group_previous_element > -1:
                self.__previous_line_groups[i] = previous_line_group_previous_element
                self.__add_cell_to_group(previous_line_group_previous_element, self.__current_height, i)

            # if the cell is connected to the above cell
            elif previous_line_group > -1:
                self.__add_cell_to_group(previous_line_group, self.__current_height, i)

            # a new group is created
            else:
                self.__create_group(i)

    def __reassign_groups(self, old_group_id, new_group_id, element_id) -> None:
        self.__groups[new_group_id].extend(self.__groups[old_group_id])
        self.__groups[old_group_id] = None
        self.__previous_line_groups[element_id] = new_group_id

        # For every group reassign, the 'groups' list must be updated accordingly
        # (some elements to the right of the current element may have the old ID)
        self.__update_indices(old_group_id, new_group_id)

    def __create_group(self, i) -> None:
        self.__groups.append([[self.__current_height, i]])
        self.__equivalent_groups.append(self.__nr_created_groups)
        self.__previous_line_groups[i] = self.__nr_created_groups
        self.__nr_created_groups += 1

    def __process_row_string(self) -> list:
        with open(self.__filename) as fd:
            for line in fd:
                row_string = line.strip()
                if row_string.endswith("],"):
                    row_string = row_string[:-1]
                if len(row_string) > 1:
                    yield json.loads(row_string)

    def output_groups(self) -> None:
        if not self.__is_matrix_processed:
            self.__process_matrix()

        for group in self.__groups:
            if group is not None and len(group) > 1:
                print(group)
