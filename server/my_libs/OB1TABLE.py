def get_start(max_len, line):
    return int(max_len/2-len(line)/2)+1


def get_end(max_len, line):
    return int(max_len/2-len(line)/2+0.5)+1


class Table:
    def __init__(self):
        self.left_up_corner = '┌'
        self.right_up_corner = '┐'
        self.left_down_corner = '└'
        self.right_down_corner = '┘'
        self.horizontal_stick = '─'
        self.vertical_stick = '│'
        self.vertical_stick_right_delimiter = '├'
        self.vertical_stick_left_delimiter = '┤'
        self.horizontal_stick_up_delimiter = '┴'
        self.horizontal_stick_down_delimiter = '┬'
        self.crossroads = '┼'
        self.columns, self.columns_list, self.lines_list = {}, [], []
        self.table = ''

    def add_columns(self, *columns):
        for column in columns:
            self.columns[column] = len(column)
            self.columns_list.append(column)

    def add_row(self, *lines):
        for column in self.columns_list:
            if self.columns_list.index(column) >= len(lines):
                line = ' '
            else:
                line = lines[self.columns_list.index(column)]
            if len(str(line)) > self.columns[column]:
                self.columns[column] = len(str(line))
            if not str(line):
                line = ' '
            self.lines_list.append(str(line))

    def add_delimiters(self, side):
        if side == 'up':
            left_corner = self.left_up_corner
            horizontal_stick_delimiter = self.horizontal_stick_down_delimiter
            right_corner = self.right_up_corner
        elif side == 'middle':
            left_corner = self.vertical_stick_right_delimiter
            horizontal_stick_delimiter = self.crossroads
            right_corner = self.vertical_stick_left_delimiter
            self.table += '\n'
        elif side == 'down':
            left_corner = self.left_down_corner
            horizontal_stick_delimiter = self.horizontal_stick_up_delimiter
            right_corner = self.right_down_corner
            self.table += '\n'
        for column in self.columns_list:
            if self.columns_list.index(column) == 0:
                self.table += left_corner
                self.table += self.horizontal_stick * (self.columns[column] + 2)
                if len(self.columns_list) > 1:
                    self.table += horizontal_stick_delimiter
            elif self.columns_list[-1] == column:
                self.table += self.horizontal_stick * (self.columns[column] + 2)
                self.table += right_corner
            else:
                self.table += self.horizontal_stick * (self.columns[column] + 2)
                self.table += horizontal_stick_delimiter
        if side != 'down' and side != 'middle':
            self.table += '\n'

    def unload_table(self, first_symbol=True):
        self.add_delimiters('up')
        for column in self.columns:
            if self.columns_list.index(column) == 0:
                self.table += self.vertical_stick
            start_line = get_start(self.columns[column], column)
            end_line = get_end(self.columns[column], column)
            self.table += ' '*start_line+column+' '*end_line+self.vertical_stick
        self.add_delimiters('middle')
        self.table += f'\n{self.vertical_stick}'
        line_num, len_lines = 0, 0
        for line in self.lines_list:
            max_line_len = self.columns[self.columns_list[line_num]]
            start_line, end_line = get_start(max_line_len, line), get_end(max_line_len, line)
            if first_symbol:
                self.table += ' '+line+' '*(end_line+start_line-1)+self.vertical_stick
            else:
                self.table += ' '*start_line+line+' '*end_line+self.vertical_stick
            line_num += 1
            len_lines += 1
            if len_lines == len(self.lines_list):
                break
            if line_num == len(self.columns_list) and line:
                self.add_delimiters('middle')
                self.table += f'\n{self.vertical_stick}'
                line_num = 0
        self.add_delimiters('down')
        table = self.table
        self.table, self.columns, self.columns_list, self.lines_list = '', {}, [], []
        return table
