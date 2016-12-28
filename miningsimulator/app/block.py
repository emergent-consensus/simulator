class Block:
    def __init__(self, parent, id, miner = None):
        self.id = id
        self.parent = parent
        if parent != None:
            self.height = parent.height + 1
        else:
            self.height = 0
        self.miner = miner
    
    def __str__(self):
        return str(self.height) + ": " + self.id.hex + " parent: " + self.parent.id.hex + " miner: " + str(self.miner.user)