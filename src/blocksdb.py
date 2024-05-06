from blockchain import Block
import aiosqlite as sqlite

class BlocksDataBase:
    conn: sqlite.Connection

    def __init__(self, db_str: str):
        self.conn = sqlite.connect(":memory:")
        
        self.conn.execute("""
          create table if not exists blocks (
              index      integer primary key
              block_json text null
          )
        """)

    def write_next_block(self, block: Block) -> None:
        #await self.conn.execute("insert into blocks (block_json) values (?)", (block.to_json(), ))
        return

    def __del__(self) -> None:
        #await self.conn.close()
        return
