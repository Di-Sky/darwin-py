import pytest
from multiprocessing import cpu_count
from darwin.utils.parallel import (
    parallel_map,
    execute_parallel_processpool,
    execute_parallel_mpire,
    MPIRE_AVAILABLE
)

def multiply(x, factor=1):
    return x * factor

def test_parallel_map_basic():
    input_data = [1, 2, 3, 4, 5]
    expected = [2, 4, 6, 8, 10]
    result = parallel_map(multiply, input_data, factor=2)
    assert result == expected

def test_parallel_map_single_worker():
    input_data = [1, 2, 3]
    expected = [2, 4, 6]
    result = parallel_map(multiply, input_data, n_workers=1, factor=2)
    assert result == expected

def test_parallel_map_auto_workers():
    input_data = [1, 2, 3]
    expected = [2, 4, 6]
    result = parallel_map(multiply, input_data, factor=2)
    assert result == expected
    
def test_parallel_map_max_workers():
    # Should not exceed CPU count
    input_data = [1, 2, 3]
    result = parallel_map(multiply, input_data, n_workers=cpu_count()+1)
    assert result == input_data

def test_processpool_execution():
    input_data = [1, 2, 3]
    expected = [2, 4, 6]
    result = execute_parallel_processpool(multiply, input_data, 2, factor=2)
    assert result == expected

@pytest.mark.skipif(not MPIRE_AVAILABLE, reason="MPIRE not installed")
def test_mpire_execution():
    input_data = [1, 2, 3]
    expected = [2, 4, 6]
    result = execute_parallel_mpire(multiply, input_data, 2, factor=2)
    assert result == expected

def test_error_handling():
    def failing_function(x):
        if x == 2:
            raise ValueError("Error on purpose")
        return x
    
    with pytest.raises(ValueError):
        parallel_map(failing_function, [1, 2, 3])

def test_empty_input():
    result = parallel_map(multiply, [])
    assert result == []

@pytest.mark.skipif(not MPIRE_AVAILABLE, reason="MPIRE not installed")
def test_mpire_import_error():
    with pytest.raises(ImportError):
        # Temporarily set MPIRE_AVAILABLE to False to test import error
        import darwin.utils.parallel as parallel
        old_mpire = parallel.MPIRE_AVAILABLE
        parallel.MPIRE_AVAILABLE = False
        try:
            execute_parallel_mpire(multiply, [1, 2, 3], 2)
        finally:
            parallel.MPIRE_AVAILABLE = old_mpire 
