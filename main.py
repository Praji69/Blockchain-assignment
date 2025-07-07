import hashlib
import json
from time import time
from typing import List, Dict, Optional

class Block:
    def __init__(self, index: int, timestamp: float, data: Dict, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # Can be transaction data or smart city records
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        
    def calculate_hash(self) -> str:
        """Calculate the SHA-256 hash of the block's contents"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def __repr__(self) -> str:
        return f"Block(index={self.index}, hash={self.hash[:10]}...)"

class SmartCityBlockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_data: List[Dict] = []
        self.initialize_genesis_block()
        
    def initialize_genesis_block(self):
        """Create the first block in the chain (genesis block)"""
        genesis_block = Block(
            index=0,
            timestamp=time(),
            data={"message": "Genesis Block for Smart City"},
            previous_hash="0"
        )
        self.chain.append(genesis_block)
    
    @property
    def last_block(self) -> Block:
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def add_data(self, sender: str, record_type: str, details: Dict):
        """Add new smart city data to be included in the next block"""
        self.pending_data.append({
            "sender": sender,
            "type": record_type,
            "details": details,
            "timestamp": time()
        })
    
    def mine_block(self) -> Block:
        """Create a new block with pending data and add it to the chain"""
        if not self.pending_data:
            raise ValueError("No pending data to mine")
        
        new_block = Block(
            index=len(self.chain),
            timestamp=time(),
            data={"transactions": self.pending_data},
            previous_hash=self.last_block.hash
        )
        
        self.chain.append(new_block)
        self.pending_data = []  # Clear the pending data
        return new_block
    
    def is_chain_valid(self) -> bool:
        """Verify the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check hash consistency
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {current_block.index} has invalid hash")
                return False
                
            # Check chain linkage
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {current_block.index} has invalid previous hash")
                return False
                
        return True
    
    def display_chain(self):
        """Print the entire blockchain"""
        for block in self.chain:
            print(f"\nBlock #{block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Previous Hash: {block.previous_hash[:10]}...")
            print(f"Hash: {block.hash[:10]}...")
            print("Data Contents:")
            for key, value in block.data.items():
                print(f"  {key}: {value}")
    
    def get_block_data_by_type(self, record_type: str) -> List[Dict]:
        """Query the blockchain for specific types of smart city records"""
        results = []
        for block in self.chain:
            if "transactions" in block.data:
                for tx in block.data["transactions"]:
                    if tx["type"] == record_type:
                        results.append(tx)
        return results

# Example Usage for Smart City Applications
if __name__ == "__main__":
    # Initialize blockchain
    city_chain = SmartCityBlockchain()
    
    # Simulate smart city data (waste management example)
    print("\nAdding smart city data to blockchain...")
    city_chain.add_data(
        sender="Resident_123",
        record_type="waste_disposal",
        details={"weight_kg": 5.2, "recycled": True, "location": "Downtown"}
    )
    
    city_chain.add_data(
        sender="Sensor_456",
        record_type="air_quality",
        details={"pm2.5": 12, "pm10": 24, "location": "Central Park"}
    )
    
    city_chain.add_data(
        sender="Vehicle_789",
        record_type="traffic",
        details={"speed": 45, "congestion": "moderate", "location": "Main Street"}
    )
    
    # Mine a new block with the pending data
    print("\nMining a new block...")
    city_chain.mine_block()
    
    # Add more data and mine another block
    city_chain.add_data(
        sender="Resident_456",
        record_type="waste_disposal",
        details={"weight_kg": 3.7, "recycled": False, "location": "Suburb A"}
    )
    
    city_chain.add_data(
        sender="Sensor_789",
        record_type="noise_level",
        details={"decibels": 68, "time": "14:30", "location": "School Zone"}
    )
    
    print("\nMining another block...")
    city_chain.mine_block()
    
    # Display the blockchain
    print("\nBlockchain Contents:")
    city_chain.display_chain()
    
    # Validate the chain
    print("\nBlockchain Valid:", city_chain.is_chain_valid())
    
    # Query specific data types
    print("\nAll Waste Disposal Records:")
    waste_records = city_chain.get_block_data_by_type("waste_disposal")
    for record in waste_records:
        print(record)
    
    print("\nAll Air Quality Records:")
    air_records = city_chain.get_block_data_by_type("air_quality")
    for record in air_records:
        print(record)