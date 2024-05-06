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

    transactions_data = [
        (b"sender1", b"reciever1", b"give 100 bulduzhnik"),
        (b"sender2", b"reciever2", b"give 100 bulduzhnik"),
        (b"sender3", b"reciever3", b"give 100 bulduzhnik"),
        (b"sender4", b"reciever4", b"give 100 bulduzhnik"),
        (b"sender5", b"reciever5", b"give 100 bulduzhnik"),
        (b"sender6", b"reciever6", b"give 100 bulduzhnik"),
        (b"sender7", b"reciever7", b"give 100 bulduzhnik"),
        (b"sender8", b"reciever8", b"give 100 bulduzhnik"),
        (b"sender9", b"reciever9", b"give 100 bulduzhnik"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender10", b"reciever10", b"give 100 huiks"),
        (b"sender11", b"reciever11", b"give 100 huiks"),
    ]

    for sender, reciever, payload in transactions_data:
        blockchain_network.process_transaction(sender, reciever, payload)

    pp(blockchain_network.blocks)

    return 0

if __name__ == "__main__":
    exit(main(argv))
