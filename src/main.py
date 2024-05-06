from sys import argv
from blockchain import Block
from miner import Miner

def main(_: list[str]) -> int:
    blocks = [Block.genesis()]

    blocks.append(Block.gen(blocks[0], b"swag on me", []))
    blocks.append(Block.gen(blocks[1], b"123ag on me", []))
    blocks.append(Block.gen(blocks[2], b"123123jag on me", []))
    blocks.append(Block.gen(blocks[3], b"swag on21123 me", []))
    blocks.append(Block.gen(blocks[4], b"swag on m123123e", []))

    return 0

if __name__ == "__main__":
    exit(main(argv))
