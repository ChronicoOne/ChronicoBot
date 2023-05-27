from os.path import exists, join

dir_path = join("..", "userData")

class User:
    def __init__(self, name):
        self.name = name.lower()
        self.filepath = join(dir_path, self.name + ".data")
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
    
    def addCoins(self, amount):
        coins = self.getCoins()

        coins += amount

        self["coins"] = str(coins)
        
        self.save()
    
    def spendCoins(self, amount):
        
        coins = self.getCoins()

        coins -= amount

        if coins >= 0:
            self["coins"] = str(coins)
            self.save()
            return True
        else:
            return False
    
    def getCoins(self):
        if "coins" in self:
            coins = int(self["coins"])
        else:
            coins = 0
        
        return coins

    def save(self):
        data_file = open(self.filepath, "w")
        
        for key in self:
            data_file.write(key + ":" + self[key] + "\n")
        
        data_file.close()
