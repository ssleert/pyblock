from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from xxhash import xxh64
from secrets import token_bytes
import json

@dataclass
class Transaction:
    id_bytes: bytes
    connected_block_hash: bytes
    timestamp: datetime
    sender_id: bytes
    reciever_id: bytes
    verificator_id: bytes
    payload: bytes
    magic_bytes: bytes
    work_hash: bytes

    @staticmethod
    def gen_random_id_bytes() -> bytes:
        return token_bytes(32)

    @staticmethod
    def get_magic_value() -> bytes:
        return token_bytes(32)

    @staticmethod
    def get_work_hash(sender: bytes, reciever: bytes, payload: bytes) -> bytes:
        return xxh64(sender + payload + reciever).digest() 

@dataclass
class Block:
    id: int
    timestamp: datetime
    previous_hash: bytes
    hash: bytes
    payload: bytes
    transactions: list[Transaction]
    transactions_hash: bytes

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    def valid(self, previous_block: Block) -> bool:
        return previous_block.hash == self.previous_hash

    @staticmethod
    def next_hash(id: int, hash: bytes, payload: bytes, transactions_hash: bytes) -> bytes:
        return xxh64(bytes(id) + hash + payload + transactions_hash).digest()

    @staticmethod
    def hash_from_transactions(transactions: list[Transaction]) -> bytes:
        hashes = list[bytes]()
        for tx in transactions:
            hashes.append(
                xxh64(
                    tx.sender_id + tx.reciever_id + tx.payload + tx.work_hash
                ).digest()
            )

        return xxh64(b"".join(hashes)).digest()

    @staticmethod
    def create(
        id: int,
        previous_hash: bytes,
    ) -> Block:
        return Block(
            id = id,
            timestamp = datetime.now(timezone.utc),
            previous_hash = previous_hash,
            hash = b"",
            payload = b"",
            transactions = [],
            transactions_hash = b"",
        )

    @staticmethod
    def gen(
        previous_block: Block,
        payload: bytes,
        transactions: list[Transaction],
    ) -> Block:
        next_block_id = previous_block.id + 1
        transactions_hash = Block.hash_from_transactions(transactions)
        next_hash = Block.next_hash(next_block_id, previous_block.hash, payload, transactions_hash)

        new_block = Block(
            id                = next_block_id,
            timestamp         = datetime.now(timezone.utc),
            previous_hash     = previous_block.hash,
            hash              = next_hash,
            payload           = payload,
            transactions      = transactions,
            transactions_hash = transactions_hash,
        )

        return new_block

    @staticmethod
    def genesis() -> Block:
        return Block(
            id                = 0,
            timestamp         = datetime.now(timezone.utc), 
            previous_hash     = b"swag on me like a shit",
            hash              = b"valeri",
            payload           = b"ur mama so fat dont flame plz",
            transactions      = [],
            transactions_hash = b"20070707",
        )
