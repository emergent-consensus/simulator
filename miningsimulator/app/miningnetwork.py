import random
from block import Block
from miners import MiningRig
import uuid
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

sysrandom = random.SystemRandom()

class MiningNetwork:

    def __init__(self, block_found_callback, block_not_found_callback):
        self.miners = []
        self.EXPECTED_INTERVAL_SECONDS = 10
        self.genesis_block = Block(None, uuid.uuid4())
        self.current_tips = [self.genesis_block]
        self._apsched = BackgroundScheduler()
        self._apsched.add_job(
            func=self.find_blocks,
            trigger=IntervalTrigger(seconds=1))
        self._apsched.start()
        self._block_found_callback = block_found_callback
        self._block_not_found_callback = block_not_found_callback

    def total_hashpower(self):
        sum = 0
        for miner in self.miners:
            sum += miner.hashpower
        return sum

    def pick_random_tip(self):
        block_saw_first = self.current_tips[sysrandom.randint(0, len(self.current_tips)-1)]
        return block_saw_first

    def find_blocks(self):
        difficulty = self.EXPECTED_INTERVAL_SECONDS * self.total_hashpower()
        new_blocks = []
        missing_miners = []
        for miner in self.miners:
            roll = sysrandom.randint(0, difficulty)
            if roll < miner.hashpower:
                found = Block(miner.mining_block, uuid.uuid4(), miner)
                new_blocks.append(found)
                miner.mining_block = found
                if self._block_found_callback != None:
                    self._block_found_callback(found)
            else:
                missing_miners.append(miner)

        num_blocks_found = len(new_blocks)
        if num_blocks_found > 0:
            self.current_tips = new_blocks
            for miner in missing_miners:
                miner.mining_block = self.pick_random_tip()
        elif self._block_not_found_callback != None:
            self._block_not_found_callback()
   
    def add_miner(self, hashpower, user):
        miner = MiningRig(100, user)
        miner.mining_block = self.pick_random_tip()
        self.miners.append(miner)