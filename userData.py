from os.path import exists, join

dir_path = join("..", "userData")

class User:
    def __init__(self, name):
        self.name = name
        self.filepath = join(dir_path, name + ".data")
        self.data_dict = {}
        self.init_file()

    def init_file(self):
        if not exists(self.filepath):
            f = open(self.filepath, "x")
            f.close()
        else:
            data_file = open(self.filepath, "r")
            for raw_line in data_file.readlines():
                line = raw_line.replace("\n", "")
                key = line.split(":")[0]
                value = line.split(":")[1]
                self[key] = value
            data_file.close()

    def __getitem__(self, key):
        return self.data_dict[key]

    def __contains__(self, key):
        return key in self.data_dict
    
    def __setitem__(self, key, value):
        self.data_dict[key] = value
    
    def __iter__(self):
        return iter(self.data_dict)

    def save(self):
        data_file = open(self.filepath, "w")
        
        for key in self:
            data_file.write(key + ":" + self[key] + "\n")
        
        data_file.close()
