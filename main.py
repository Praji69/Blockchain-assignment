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

     def generate_hash(self):
        # Creates a unique hash for this block
        # All block information is combined to make the hash
        block_content = {
            "id": self.block_id,
            "prev_hash": self.prev_block_hash,
            "timestamp": self.created_time,
            "data": self.block_data,
            "nonce": self.nonce
        }
        # Convert to string and create hash
        content_string = json.dumps(block_content, sort_keys=True)
        return hashlib.sha256(content_string.encode('utf-8')).hexdigest()
    
    # Main blockchain class
class SecureChain:
    """
    The blockchain system that manages all blocks.
    Provides mining and validation functionaliy.
    """
    def __init__(self):
        self.blocks = [self.initialize_genesis()]   # Start with first block
        self.mining_complexity = 3                  # Difficulty level for mining

    def initialize_genesis(self):
        # Creates the first block in the blockchain
        # This block has no previous block to reference
        return CryptoBlock(0, "0x0", time.time(), "Genesis Block - First block created", 0)

    def fetch_last_block(self):
        # Returns the most recent block in the chain
        return self.blocks[-1]

    def mine_block(self, target_block):
        # Performs mining operation on a block
        # Mining finds a nonce that makes the hash start with zeros
        target_block.nonce = 0
        mining_target = "0" * self.mining_complexity