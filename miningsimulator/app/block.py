class Block:
    def __init__(self, parent, id):
        self.id = id
        self.parent = parent
        if parent != None:
            self.height = parent.height + 1
        else:
            self.height = 0
