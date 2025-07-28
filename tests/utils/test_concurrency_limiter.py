import pytest

from utils.concurrency_limiter import ConcurrencyLimiter


class TestConcurrencyLimiter:
    @pytest.fixture
    def limiter(self):
        return ConcurrencyLimiter(max_concurrent=2)

    async def test_execute_tasks_success(self, limiter):
        async def mock_task(value):
            return value * 2

        tasks = [mock_task(1), mock_task(2), mock_task(3)]

        results = await limiter.execute_tasks(tasks)

        assert results == [2, 4, 6]

    async def test_execute_tasks_with_exception(self, limiter):
        async def failing_task():
            raise ValueError("Task failed")

        async def success_task():
            return "success"

        tasks = [success_task(), failing_task()]

        with pytest.raises(ValueError, match="Task failed"):
            await limiter.execute_tasks(tasks)
