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
        print(f"Mining started with difficulty {self.mining_complexity}")
        start_time = time.time()
        
        while True:
            # Calculate new hash with current nonce
            target_block.current_hash = target_block.generate_hash()
            # Check if hash meets the difficulty requirement
            if target_block.current_hash.startswith(mining_target):
                mining_time = time.time() - start_time
                print(f"Block mined successfully in {mining_time:.2f} seconds")
                print(f"Final nonce value: {target_block.nonce}")
                break
            target_block.nonce += 1
            
            # Show progress every 5000 attempts
            if target_block.nonce % 5000 == 0:
                print(f"Mining in progress... attempts made: {target_block.nonce}")

    def append_new_block(self, user_data):
        """
        Creates a new block with user data and adds it to the chain.
        The block must be mined before adding to the blockchain.
        """
        # Get hash from the last block to link properly
        last_block_hash = self.fetch_last_block().current_hash
        # Create new block with provided data
        new_crypto_block = CryptoBlock(
            block_id=len(self.blocks),
            prev_block_hash=last_block_hash,
            created_time=time.time(),
            block_data=user_data,
            nonce=0
        )
        self.mine_block(new_crypto_block)           # Mine the block
        self.blocks.append(new_crypto_block)        # Add to chain

    def validate_integrity(self):
        """
        Checks if the blockchain is valid and not tampered with.
        Verifies all hashes and block connections.
        """
        print("Checking blockchain integrity...")
        
        # Check each block starting from second block
        for i in range(1, len(self.blocks)):
            current_block = self.blocks[i]
            previous_block = self.blocks[i-1]

            # Verify the stored hash matches calculated hash
            if current_block.current_hash != current_block.generate_hash():
                print(f"Block {current_block.block_id}: Hash does not match!")
                return False
            
            # Verify the block links to previous block correctly
            if current_block.prev_block_hash != previous_block.current_hash:
                print(f"Block {current_block.block_id}: Previous hash link is broken!")
                return False