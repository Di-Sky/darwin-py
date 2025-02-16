from typing import Callable, Iterable, List, Optional, TypeVar
import concurrent.futures
from multiprocessing import cpu_count

try:
    from mpire.pool import WorkerPool
    MPIRE_AVAILABLE = True
except ImportError:
    MPIRE_AVAILABLE = False

T = TypeVar('T')
R = TypeVar('R')

def execute_parallel_mpire(
    func: Callable[[T], R],
    iterable: Iterable[T],
    n_workers: int,
    **kwargs
) -> List[R]:
    """
    Execute a function in parallel using MPIRE WorkerPool.
    
    Parameters
    ----------
    func : Callable[[T], R]
        Function to execute in parallel
    iterable : Iterable[T]
        Input data to process
    n_workers : int
        Number of worker processes
    **kwargs
        Additional keyword arguments to pass to the worker function
        
    Returns
    -------
    List[R]
        List of results from parallel execution
    """
    if not MPIRE_AVAILABLE:
        raise ImportError("MPIRE is not installed. Please install it using `pip install mpire`.")
    with WorkerPool(n_workers) as pool:
        if kwargs:
            results = pool.map(
                lambda x: func(x, **kwargs),
                iterable
            )
        else:
            results = pool.map(func, iterable)
        return list(results)


def execute_parallel_processpool(
    func: Callable[[T], R],
    iterable: Iterable[T],
    n_workers: int,
    **kwargs
) -> List[R]:
    """
    Execute a function in parallel using ProcessPoolExecutor.
    
    Parameters
    ----------
    func : Callable[[T], R]
        Function to execute in parallel
    iterable : Iterable[T]
        Input data to process
    n_workers : int
        Number of worker processes
    **kwargs
        Additional keyword arguments to pass to the worker function
        
    Returns
    -------
    List[R]
        List of results from parallel execution
    """
    with concurrent.futures.ProcessPoolExecutor(max_workers=n_workers) as executor:
        if kwargs:
            future_to_result = {
                executor.submit(func, item, **kwargs): item 
                for item in iterable
            }
        else:
            future_to_result = {
                executor.submit(func, item): item 
                for item in iterable
            }
        
        results = []
        for future in concurrent.futures.as_completed(future_to_result):
            results.append(future.result())
            
        return results


def parallel_map(
    func: Callable[[T], R],
    iterable: Iterable[T],
    n_workers: Optional[int] = None,
    use_mpire: bool = True,
    **kwargs
) -> List[R]:
    """
    Maps a function over an iterable in parallel using either MPIRE or ProcessPoolExecutor.
    
    Parameters
    ----------
    func : Callable[[T], R]
        Function to execute in parallel
    iterable : Iterable[T]
        Input data to process
    n_workers : Optional[int]
        Number of worker processes. If None, uses CPU count - 1
    use_mpire : bool
        Whether to prefer MPIRE over ProcessPoolExecutor when available
    **kwargs
        Additional keyword arguments to pass to the worker function
        
    Returns
    -------
    List[R]
        List of results from parallel execution
    
    Examples
    --------
    >>> def process_item(x, multiplier=1):
    ...     return x * multiplier
    >>> items = [1, 2, 3, 4, 5]
    >>> results = parallel_map(process_item, items, multiplier=2)
    >>> print(results)
    [2, 4, 6, 8, 10]
    """
    # Determine number of workers
    if n_workers is None:
        n_workers = max(1, cpu_count() - 1)
    n_workers = min(n_workers, cpu_count())

    # Skip parallel processing if only 1 worker
    if n_workers <= 1:
        return [func(item, **kwargs) for item in iterable]

    # Use MPIRE if available and requested
    if use_mpire and MPIRE_AVAILABLE:
        return execute_parallel_mpire(func, iterable, n_workers, **kwargs)

    # Fall back to ProcessPoolExecutor
    return execute_parallel_processpool(func, iterable, n_workers, **kwargs) 
