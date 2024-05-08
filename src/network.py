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

    def __init__(self, processors_amount_percentage: int = 20, transactions_per_block: int = 1000) -> None:
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

    def check_retryes(self, retryes: int) -> None:
        if retryes == 0:
            raise Network.LegitimateHashVerificationError()

    def get_processors_amount(self) -> int:
        miners_amount = len(self.miners)
        if miners_amount == 0:
            raise Network.MinersPoolEmpty()

        amount_of_processors_for_transaction = ceil((miners_amount / 100) * self.processors_amount_percentage)

        return amount_of_processors_for_transaction

    def get_miners_in_random_order(self) -> dict[bytes, Miner]: 
        miners_ids_in_random_order = list(self.miners.keys())
        shuffle(miners_ids_in_random_order)
        miners_in_random_order = {miner_id: self.miners[miner_id] for miner_id in miners_ids_in_random_order}
        return miners_in_random_order

    def process_transaction_with_miners(
        self, 
        transaction_input_data: Miner.TransactionInputData,
        miners: dict[bytes, Miner], 
        processors_amount: int,
    ) -> dict[bytes, Miner.TransactionOutputData]:
        miners_for_transaction = processors_amount
        output_data = dict[bytes, Miner.TransactionOutputData]()
        for miner_id, miner in miners.items():
            if miners_for_transaction == 0:
                break
            
            out = miner.process_transaction(transaction_input_data)
            if (transaction_input_data.id_bytes != out.id_bytes 
                or out.magic_value != transaction_input_data.magic_value):
                continue

            output_data[miner_id] = out
            miners_for_transaction -= 1

        return output_data

    def get_legitimate_hash_from_transaction_output_data(
        self, 
        miners_output_data: dict[bytes, Miner.TransactionOutputData],
    ) -> bytes:
        hashes_occurrence = dict[bytes, int]() 
        for _, data in miners_output_data.items():
            if data.work_hash not in hashes_occurrence:
                hashes_occurrence[data.work_hash] = 1
            else: 
                hashes_occurrence[data.work_hash] += 1

        return max(hashes_occurrence, key=lambda k: hashes_occurrence[k])

    def verify_transaction_with_random_miner(
        self, 
        transaction_input_data: Miner.TransactionInputData, 
        legitimate_hash: bytes,
    ) -> tuple[bool, bytes]:
        hash_verificator = choice(list(self.miners.keys())) # TODO: rewrite with check is miner processed the same transaction
        verification_transaction_output = self.miners[hash_verificator].process_transaction(transaction_input_data)
        return (verification_transaction_output.work_hash == legitimate_hash, hash_verificator)

    def create_new_block_if_needed(self, payload: bytes) -> None:
        if len(self.current_transactions) == self.transactions_per_block:
            block = Block.gen(
                previous_block = self.previous_block,
                payload        = payload, # TODO: normal payload :(
                transactions   = self.current_transactions
            )
            self.current_transactions = []

            self.blocks.append(block)
            self.previous_block = block
            self.broadcast_previous_block_to_miners()

    def process_transaction(self, sender_id: bytes, reciever_id: bytes, payload: bytes, retryes: int = 3) -> None:
        self.check_retryes(retryes)

        processors_amount = self.get_processors_amount()
        miners_in_random_order = self.get_miners_in_random_order()

        current_transaction_input_data = Miner.TransactionInputData(
            id_bytes = Transaction.gen_random_id_bytes(),
            connected_block_hash = self.previous_block.hash,
            sender_id = sender_id,
            reciever_id = reciever_id,
            payload = payload,
            magic_value = Transaction.get_magic_value(),
        )

        transaction_processors_output_data = self.process_transaction_with_miners(
            current_transaction_input_data,
            miners_in_random_order, 
            processors_amount
        )

        legitimate_hash = self.get_legitimate_hash_from_transaction_output_data(transaction_processors_output_data)
        hash_valid, verificator_id = self.verify_transaction_with_random_miner(current_transaction_input_data, legitimate_hash)

        if not hash_valid:
            self.process_transaction(sender_id, reciever_id, payload, retryes - 1)

        self.current_transactions.append(Transaction(
             id_bytes             = current_transaction_input_data.id_bytes,
             connected_block_hash = current_transaction_input_data.connected_block_hash,
             timestamp            = datetime.now(timezone.utc),
             sender_id            = current_transaction_input_data.sender_id,
             reciever_id          = current_transaction_input_data.reciever_id,
             verificator_id       = verificator_id,
             payload              = current_transaction_input_data.payload,
             magic_bytes          = current_transaction_input_data.magic_value,
             work_hash            = legitimate_hash,
        ))

        self.create_new_block_if_needed(b"i love u :)")
