"""
Unit tests for BlockManager

This module tests the KV Cache block management functionality,
including allocation, deallocation, and memory utilization.
"""

import pytest
# from mini_infer.memory.block_manager import BlockManager


class MockBlockManager:
    """
    Mock BlockManager for testing structure.
    Replace with actual implementation when ready.
    """
    def __init__(self, block_size: int, num_blocks: int):
        self.block_size = block_size
        self.num_blocks = num_blocks
        self.free_blocks = list(range(num_blocks))
        self.allocated_blocks = set()
    
    def allocate(self, num_blocks: int):
        """Allocate blocks"""
        if len(self.free_blocks) < num_blocks:
            raise RuntimeError("Out of memory: not enough free blocks")
        
        blocks = []
        for _ in range(num_blocks):
            block = self.free_blocks.pop(0)
            self.allocated_blocks.add(block)
            blocks.append(block)
        return blocks
    
    def free(self, blocks):
        """Free blocks"""
        for block in blocks:
            if block in self.allocated_blocks:
                self.allocated_blocks.remove(block)
                self.free_blocks.append(block)
    
    def get_num_free_blocks(self):
        """Get number of free blocks"""
        return len(self.free_blocks)
    
    def get_fragmentation(self):
        """Calculate fragmentation ratio"""
        # Simple fragmentation metric
        if not self.free_blocks:
            return 0.0
        gaps = 0
        sorted_free = sorted(self.free_blocks)
        for i in range(len(sorted_free) - 1):
            if sorted_free[i+1] - sorted_free[i] > 1:
                gaps += 1
        return gaps / len(sorted_free) if sorted_free else 0.0


class TestBlockManager:
    """Test suite for BlockManager"""
    
    def setup_method(self):
        """Setup before each test"""
        self.block_size = 16
        self.num_blocks = 100
        # Replace MockBlockManager with actual BlockManager when implemented
        self.manager = MockBlockManager(
            block_size=self.block_size,
            num_blocks=self.num_blocks
        )
    
    def test_initialization(self):
        """Test BlockManager initialization"""
        assert self.manager.block_size == self.block_size
        assert self.manager.num_blocks == self.num_blocks
        assert self.manager.get_num_free_blocks() == self.num_blocks
    
    def test_allocation(self):
        """Test block allocation"""
        # Allocate blocks
        blocks = self.manager.allocate(num_blocks=10)
        
        assert len(blocks) == 10
        assert all(isinstance(b, int) for b in blocks)
        assert len(set(blocks)) == 10  # All unique
        assert self.manager.get_num_free_blocks() == self.num_blocks - 10
    
    def test_deallocation(self):
        """Test block deallocation"""
        # Allocate blocks
        blocks = self.manager.allocate(num_blocks=10)
        free_before = self.manager.get_num_free_blocks()
        
        # Free blocks
        self.manager.free(blocks)
        free_after = self.manager.get_num_free_blocks()
        
        assert free_after == free_before + 10
    
    def test_out_of_memory(self):
        """Test OOM handling"""
        # Allocate all blocks
        blocks = self.manager.allocate(num_blocks=self.num_blocks)
        
        # Try to allocate more
        with pytest.raises(RuntimeError, match="Out of memory"):
            self.manager.allocate(num_blocks=1)
    
    def test_multiple_allocations(self):
        """Test multiple allocation and deallocation cycles"""
        for _ in range(10):
            blocks = self.manager.allocate(num_blocks=5)
            assert len(blocks) == 5
            self.manager.free(blocks[:2])  # Free some blocks
            assert self.manager.get_num_free_blocks() > 0
    
    def test_fragmentation(self):
        """Test fragmentation calculation"""
        # Allocate and free randomly to create fragmentation
        for _ in range(20):
            blocks = self.manager.allocate(num_blocks=5)
            self.manager.free(blocks[:2])
        
        fragmentation = self.manager.get_fragmentation()
        # Fragmentation should be a valid ratio
        assert 0.0 <= fragmentation <= 1.0
    
    def test_allocate_zero_blocks(self):
        """Test allocating zero blocks"""
        blocks = self.manager.allocate(num_blocks=0)
        assert len(blocks) == 0
        assert self.manager.get_num_free_blocks() == self.num_blocks
    
    def test_free_empty_list(self):
        """Test freeing empty list"""
        initial_free = self.manager.get_num_free_blocks()
        self.manager.free([])
        assert self.manager.get_num_free_blocks() == initial_free
    
    def test_large_allocation(self):
        """Test large allocation"""
        large_size = self.num_blocks // 2
        blocks = self.manager.allocate(num_blocks=large_size)
        assert len(blocks) == large_size
        assert self.manager.get_num_free_blocks() == self.num_blocks - large_size


@pytest.mark.slow
class TestBlockManagerPerformance:
    """Performance tests for BlockManager"""
    
    def test_allocation_performance(self):
        """Test allocation performance with large number of blocks"""
        manager = MockBlockManager(block_size=16, num_blocks=10000)
        
        import time
        start = time.time()
        for _ in range(100):
            blocks = manager.allocate(num_blocks=50)
            manager.free(blocks)
        elapsed = time.time() - start
        
        # Should complete in reasonable time
        assert elapsed < 1.0  # Less than 1 second


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
