from __future__ import annotations
from math import ceil
from datetime import datetime, timezone
from miner import Miner
from random import shuffle, choice
from blockchain import Block, Transaction

class Network:
    class MinersPoolEmpty(Exception):
        def __init__(self) -> None:
            super().__init__("Miner pool empty. Cant process transaction.")

    class LegitimateHashVerificationError(Exception):
        def __init__(self) -> None:
            super().__init__("Cant verificate legitimate hash.")

    blocks: list[Block]
    miners: dict[bytes, Miner]
    previous_block: Block

    current_transactions: list[Transaction]

    processors_amount_percentage: int
    transactions_per_block: int

    def __init__(self, processors_amount_percentage: int = 20, transactions_per_block: int = 30) -> None:
        self.blocks = [Block.genesis()]
        self.miners = {}
        self.previous_block = self.blocks[0]

        self.current_transactions = []

        self.processors_amount_percentage = processors_amount_percentage
        self.transactions_per_block = transactions_per_block

    def broadcast_previous_block_to_miners(self) -> None:
        for _, miner in self.miners.items():
            miner.broadcast_new_block(self.previous_block)

    def connect_miner(self, miner_id: bytes, miner: Miner) -> None:
        self.miners[miner_id] = miner
    
    def disconnect_miner(self, miner_id: bytes) -> None:
        del self.miners[miner_id]

    def process_transaction(self, sender_id: bytes, reciever_id: bytes, payload: bytes, retryes: int = 3) -> None:
        if retryes == 0:
            raise Network.LegitimateHashVerificationError()

        miners_amount = len(self.miners)
        amount_of_miners_for_transaction = ceil((miners_amount / 100) * 20)

        if miners_amount == 0:
            raise Network.MinersPoolEmpty()

        miners_ids_in_random_order = list(self.miners.keys())
        shuffle(miners_ids_in_random_order)
        miners_in_random_order = {miner_id: self.miners[miner_id] for miner_id in miners_ids_in_random_order}

        current_transaction_input_data = Miner.TransactionInputData(
            id_bytes = Transaction.gen_random_id_bytes(),
            connected_block_hash = self.previous_block.hash,
            sender_id = sender_id,
            reciever_id = reciever_id,
            payload = payload,
            magic_value = Transaction.get_magic_value(),
        )

        transaction_processors_output_data = dict[bytes, Miner.TransactionOutputData]()
        for miner_id, miner in miners_in_random_order.items():
            if amount_of_miners_for_transaction == 0:
                break

            out = miner.process_transaction(current_transaction_input_data) 
            if (current_transaction_input_data.id_bytes != out.id_bytes 
                or out.magic_value != current_transaction_input_data.magic_value):
                continue

            transaction_processors_output_data[miner_id] = out

            amount_of_miners_for_transaction -= 1

        hashes_occurrence = dict[bytes, int]() 
        for miner_id, data in transaction_processors_output_data.items():
            if data.work_hash not in hashes_occurrence:
                hashes_occurrence[data.work_hash] = 1
            else: 
                hashes_occurrence[data.work_hash] += 1

        legitimate_hash = max(hashes_occurrence, key=lambda k: hashes_occurrence[k])
        hash_verificator = choice(list(self.miners.keys())) # TODO: rewrite with check is miner processed the same transaction
     
        verification_transaction_output = self.miners[hash_verificator].process_transaction(current_transaction_input_data)

        if verification_transaction_output.work_hash != legitimate_hash:
            self.process_transaction(sender_id, reciever_id, payload, retryes - 1)

        self.current_transactions.append(Transaction(
             id_bytes             = current_transaction_input_data.id_bytes,
             connected_block_hash = current_transaction_input_data.connected_block_hash,
             timestamp            = datetime.now(timezone.utc),
             sender_id            = current_transaction_input_data.sender_id,
             reciever_id          = current_transaction_input_data.reciever_id,
             verificator_id       = hash_verificator,
             payload              = current_transaction_input_data.payload,
             magic_bytes          = current_transaction_input_data.magic_value,
             work_hash            = legitimate_hash,
        ))

        if len(self.current_transactions) == self.transactions_per_block - 1:
            block = Block.gen(
                previous_block = self.previous_block,
                payload        = b"i love u", # TODO: normal payload :(
                transactions   = self.current_transactions
            )
            self.current_transactions = []

            self.blocks.append(block)
            self.previous_block = block
            self.broadcast_previous_block_to_miners()


