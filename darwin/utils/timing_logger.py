from time import perf_counter
from typing import Union, Optional
from logging import Logger
from rich.console import Console

class MaybeConsole:
    """
    A class that handles console/logger output with timing information.
    
    This class provides a callable interface that prints messages with elapsed time
    either to a Rich console or a logger. Each call starts its own timer.
    
    Parameters
    ----------
    logger : Logger
        Logger instance to use when console is None
    console : Optional[Console], optional
        Rich console to print to. If None, uses logger.info
        
    Examples
    --------
    >>> logger = getLogger(__name__)
    >>> console = Console()
    >>> printer = MaybeConsole(logger, console)
    >>> printer("Starting process...")  # Prints with elapsed time
    """
    
    def __init__(self, logger: Logger, console: Optional[Console] = None):
        self.logger = logger
        self.console = console
        self.reset()
    
    def _get_elapsed_time(self) -> float:
        """
        Get the elapsed time since the timer was started.
        
        Returns
        -------
        float
            Elapsed time in seconds
        """
        return perf_counter() - self.start_time
    
    def reset(self) -> None:
        """
        Reset the timer.
        """
        self.start_time = perf_counter()
    
    def __call__(self, *args: Union[str, int, float]) -> None:
        """
        Print messages with timing information.
        
        Parameters
        ----------
        *args : Union[str, int, float]
            Messages to print
        """
        elapsed = self._get_elapsed_time()

        if self.console is not None:
            self.console.print(*[f"[{str(elapsed)} seconds elapsed]", *args])
        else:
            message = " ".join(str(arg) for arg in [f"[{str(elapsed)}]", *args])
            self.logger.info(message) 
