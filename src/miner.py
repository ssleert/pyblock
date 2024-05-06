from __future__ import annotations
from dataclasses import dataclass
from blockchain import Block, Transaction

class Miner:
    @dataclass
    class TransactionInputData:
        id_bytes: bytes
        connected_block_hash: bytes
        sender_id: bytes
        reciever_id: bytes
        payload: bytes
        magic_value: bytes

    @dataclass
    class TransactionOutputData:
        id_bytes: bytes
        work_hash: bytes
        magic_value: bytes

    class InvalidBroadcastedBlockError(Exception):
        def __init__(self) -> None:
            super().__init__("Broadcasted block invalid.")

    class InvalidConnectedBlockForTransaction(Exception):
        def __init__(self) -> None:
            super().__init__("Invalid connected block hash on transaction.")

    blocks: list[Block]
    previous_block: Block | None

    def __init__(self) -> None:
        self.blocks = []
        self.previous_block = None

    def process_transaction(self, input: TransactionInputData) -> TransactionOutputData:
        if self.previous_block is not None:
            if self.previous_block.hash != input.connected_block_hash:
                raise Miner.InvalidConnectedBlockForTransaction()

        work_hash = Transaction.get_work_hash(
            input.sender_id, 
            input.reciever_id, 
            input.payload,
        )
        return Miner.TransactionOutputData(
            id_bytes = input.id_bytes, 
            work_hash = work_hash, 
            magic_value = input.magic_value
        )

    def broadcast_new_block(self, block: Block) -> None:
        if self.previous_block is not None:
            if not block.valid(self.previous_block):
                raise Miner.InvalidBroadcastedBlockError();

        self.previous_block = block
        self.blocks.append(block)
