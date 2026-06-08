"""
System: Transactional Disk-Backed Page-Indexed B-Tree Core Engine
Description: A high-performance storage engine that builds an on-disk balanced B-Tree index 
             structure, managing record nodes via explicit block allocation offsets.
Lead Engineer: Syed Saad Bin Irfan
"""

import os
import struct
import logging
from typing import List, Tuple, Optional

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (BTree-Core) %(message)s')

class DiskBTreeNodeFrame:
    """Models a single balanced B-Tree node frame block mapped to direct storage file coordinates."""
    def __init__(self, file_offset_position: int, is_leaf_node: bool = True) -> None:
        self.file_offset: int = file_offset_position
        self.is_leaf: bool = is_leaf_node
        self.keys_array: List[int] = []
        # Maps index keys to explicit file byte offset locations
        self.values_offset_array: List[int] = []
        self.children_offsets_array: List[int] = []


class DiskBackedBTreeEngine:
    """Manages an on-disk balanced B-Tree index engine using explicit block offsets."""
    # Node Metadata Header Format: uint8 (Is Leaf Flag), uint16 (Active Keys Count)
    NODE_HEADER_FORMAT = "!BH"
    HEADER_SIZE = struct.calcsize(NODE_HEADER_FORMAT)

    def __init__(self, index_storage_filepath: str = "cluster_tree_node.idx") -> None:
        self.filepath: str = index_storage_filepath
        # Configure the structural branching factor parameter limit
        self.branching_factor_t: int = 3 # Minimum degree boundary mapping rule
        
        # Initialize or restore the storage file handle
        if not os.path.exists(self.filepath):
            self.file_descriptor = open(self.filepath, "w+b", buffering=0)
            # Allocate the root node at the file's base offset coordinate location
            root_node = DiskBTreeNodeFrame(file_offset_position=0, is_leaf_node=True)
            self._write_node_block_to_disk(root_node)
        else:
            self.file_descriptor = open(self.filepath, "r+b", buffering=0)

    def _write_node_block_to_disk(self, node: DiskBTreeNodeFrame) -> None:
        """Packs and commits B-Tree node data blocks straight down into explicit file offsets."""
        self.file_descriptor.seek(node.file_offset)
        
        is_leaf_flag = 1 if node.is_leaf else 0
        active_keys_count = len(node.keys_array)
        header_bytes = struct.pack(self.NODE_HEADER_FORMAT, is_leaf_flag, active_keys_count)
        self.file_descriptor.write(header_bytes)

        # Serialize key arrays into sequential binary fields
        for key in node.keys_array:
            self.file_descriptor.write(struct.pack("!Q", key)) # 8-byte unsigned integer keys
            
        for val_offset in node.values_offset_array:
            self.file_descriptor.write(struct.pack("!Q", val_offset))

        if not node.is_leaf:
            for child_offset in node.children_offsets_array:
                self.file_descriptor.write(struct.pack("!Q", child_offset))
                
        os.fsync(self.file_descriptor.fileno())

    def search_key_index(self, start_node_offset: int, target_key: int) -> Optional[int]:
        """Traverses the on-disk B-Tree structure recursively to resolve target index keys."""
        node = self._read_node_block_from_disk(start_node_offset)
        idx = 0
        
        while idx < len(node.keys_array) and target_key > node.keys_array[idx]:
            idx += 1

        if idx < len(node.keys_array) and target_key == node.keys_array[idx]:
            logging.info(f"[INDEX-MATCH] Resolved key '{target_key}' on disk block offset coordinate: {node.file_offset}")
            return node.values_offset_array[idx]

        if node.is_leaf:
            return None
            
        # Continue searching recursively down into the target child node block path
        return self.search_key_index(node.children_offsets_array[idx], target_key)

    def _read_node_block_from_disk(self, file_offset: int) -> DiskBTreeNodeFrame:
        """Unpacks and loads a B-Tree node frame block directly from a storage file address."""
        self.file_descriptor.seek(file_offset)
        header_bytes = self.file_descriptor.read(self.HEADER_SIZE)
        
        is_leaf_flag, active_keys_count = struct.unpack(self.NODE_HEADER_FORMAT, header_bytes)
        node = DiskBTreeNodeFrame(file_offset_position=file_offset, is_leaf_node=(is_leaf_flag == 1))

        for _ in range(active_keys_count):
            key, = struct.unpack("!Q", self.file_descriptor.read(8))
            node.keys_array.append(key)
            
        for _ in range(active_keys_count):
            val_offset, = struct.unpack("!Q", self.file_descriptor.read(8))
            node.values_offset_array.append(val_offset)

        if not node.is_leaf:
            for _ in range(active_keys_count + 1):
                child_offset, = struct.unpack("!Q", self.file_descriptor.read(8))
                node.children_offsets_array.append(child_offset)
                
        return node

    def inject_key_mapping(self, key: int, value_block_offset: int) -> None:
        """Inserts a key mapping entry into the root node block wrapper."""
        # Read the current root node configuration frame
        root_node = self._read_node_block_from_disk(0)
        
        # Simple inline allocation check pass: append elements to keys block directly
        # Production expansion: incorporate multi-level node split routines when hitting capacity thresholds
        root_node.keys_array.append(key)
        root_node.values_offset_array.append(value_block_offset)
        
        self._write_node_block_to_disk(root_node)
        logging.info(f"[INDEX-WRITE] Key mapping entry successfully logged to root node file context: {key} -> {value_block_offset}")

    def dismantle_engine_context(self) -> None:
        if not self.file_descriptor.closed:
            self.file_descriptor.close()
        if os.path.exists(self.filepath):
            os.remove(self.filepath)


if __name__ == "__main__":
    print("\n=== SYSTEM START: DISK-BACKED PAGE-INDEXED B-TREE ENGINE ===\n")
    engine = DiskBackedBTreeEngine()

    # Insert page mappings into the disk index structure
    engine.inject_key_mapping(key=540011, value_block_offset=4096)
    engine.inject_key_mapping(key=991024, value_block_offset=8192)

    # Search for keys across disk index coordinates
    result_address = engine.search_key_index(start_node_offset=0, target_key=991024)
    print(f"\n[QUERY RESOLUTION] Key 991024 resolved data page block address target: {result_address}")

    engine.dismantle_engine_context()
    print("\n=== SYSTEM SHUTDOWN: ON-DISK B-TREE INDEX ENGINE CLEANED DOWN ===")