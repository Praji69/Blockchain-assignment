import hashlib  # Module for creating secure hash functions
import time     # Module for time operations
import json     # Module for JSON data handling

# Block Definition
class CryptoBlock:
    """
    A single block in the blockchain.
    Each block contains data and links to the previous block.
    """
    def __init__(self, block_id, prev_block_hash, created_time, block_data, nonce):
        self.block_id = block_id                    # Position of block in the chain
        self.prev_block_hash = prev_block_hash      # Hash of the previous block
        self.created_time = created_time            # When the block was created
        self.block_data = block_data                # Data stored in this block
        self.nonce = nonce                          # Number used for mining
        self.current_hash = self.generate_hash()    # Hash of this block

    