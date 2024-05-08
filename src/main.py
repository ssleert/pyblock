from sys import argv
from blockchain import Block
from miner import Miner
from network import Network
from pprint import pp

def main(_: list[str]) -> int:
    blockchain_network = Network()
    miners_pool = {
        b"abcd1": Miner(),
        b"abcd2": Miner(),
        b"abcd3": Miner(),
        b"abcd4": Miner(),
        b"abcd5": Miner(),
        b"abcd6": Miner(),
        b"abcd7": Miner(),
        b"abcd8": Miner(),
        b"abcd9": Miner(),
        b"abcd10": Miner(),
    }

    for key, val in miners_pool.items():
        blockchain_network.connect_miner(key, val)

    for i in range(0, 100000):
        blockchain_network.process_transaction(b"simon", b"*******", b"love")

    pp(blockchain_network.blocks)

    return 0

if __name__ == "__main__":
    exit(main(argv))
