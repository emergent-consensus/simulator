class MiningRig:

    def __init__(self, hashpower, user):
        self.hashpower = hashpower
        self.mining_block = None
        self.user = user

    def __str__(self):
        return "Mining Rig Hashpower " + str(self.hashpower) + " owned by " + str(self.user)