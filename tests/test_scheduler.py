"""
Unit tests for Scheduler

This module tests the continuous batching scheduler functionality.
"""

import pytest
from typing import List


class MockSchedulerRequest:
    """Mock scheduler request for testing"""
    def __init__(self, request_id: str, prompt: str, max_tokens: int, priority: int = 0):
        self.request_id = request_id
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.priority = priority
        self.num_generated_tokens = 0
        self.is_finished = False


class MockScheduler:
    """Mock Scheduler - replace with actual implementation"""
    def __init__(self, max_num_seqs: int):
        self.max_num_seqs = max_num_seqs
        self.waiting_queue: List[MockSchedulerRequest] = []
        self.running_queue: List[MockSchedulerRequest] = []
    
    def add_request(self, request: MockSchedulerRequest):
        self.waiting_queue.append(request)
    
    def schedule(self) -> List[MockSchedulerRequest]:
        scheduled = []
        while len(self.running_queue) < self.max_num_seqs and self.waiting_queue:
            self.waiting_queue.sort(key=lambda x: x.priority, reverse=True)
            request = self.waiting_queue.pop(0)
            self.running_queue.append(request)
            scheduled.append(request)
        return scheduled
    
    def get_num_waiting(self) -> int:
        return len(self.waiting_queue)
    
    def get_num_running(self) -> int:
        return len(self.running_queue)


class TestScheduler:
    """Test suite for Scheduler"""
    
    def setup_method(self):
        self.scheduler = MockScheduler(max_num_seqs=4)
    
    def test_initialization(self):
        assert self.scheduler.max_num_seqs == 4
        assert self.scheduler.get_num_waiting() == 0
    
    def test_add_request(self):
        req = MockSchedulerRequest("req_1", "Hello", 10)
        self.scheduler.add_request(req)
        assert self.scheduler.get_num_waiting() == 1
    
    def test_schedule_multiple(self):
        for i in range(6):
            self.scheduler.add_request(MockSchedulerRequest(f"req_{i}", "prompt", 10))
        scheduled = self.scheduler.schedule()
        assert len(scheduled) == 4
        assert self.scheduler.get_num_running() == 4
    
    def test_priority_scheduling(self):
        reqs = [
            MockSchedulerRequest("low", "p", 10, priority=1),
            MockSchedulerRequest("high", "p", 10, priority=10),
        ]
        for req in reqs:
            self.scheduler.add_request(req)
        scheduled = self.scheduler.schedule()
        assert scheduled[0].request_id == "high"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
