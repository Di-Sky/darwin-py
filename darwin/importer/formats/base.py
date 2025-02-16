from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Union

from darwin.datatypes import AnnotationFile

class BaseImportParser(ABC):
    """Abstract base class for all parsers."""

    @staticmethod
    @abstractmethod
    def parse_path(path: Path) -> Union[List[AnnotationFile], AnnotationFile, None]:
        """Parses the given file path and returns structured data."""
        pass
