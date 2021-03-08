class PCBData:
    def __init__(self, filepath):
        self.filepath = filepath
        self.pcb_width = 0
        self.pcb_height = 0
        self.pcb_path_points = []

    def read_file(self):
        with open(self.filepath) as fp:
            for cnt, line in enumerate(fp):
                line_values = line.split(";")
                if cnt == 0:
                    self.pcb_width = int(line_values[0])
                    self.pcb_height = int(line_values[1])
                else:
                    self.pcb_path_points.append([int(line_values[index]) for index in range(4)])

