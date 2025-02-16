from pathlib import Path
from typing import Union, List

import darwin.datatypes as dt
from darwin.utils import parse_darwin_json
from .base import BaseImportParser


class Parser(BaseImportParser):

    @staticmethod
    def parse_path(path: Path) -> Union[List[dt.AnnotationFile], dt.AnnotationFile, None]:
        """
        Parses the given file into a darwin ``AnnotationFile`` or returns ``None`` if the file does not
        have a ``.json`` extension.

        Parameters
        ----------
        path : Path
            The ``Path`` of the file to parse.

        Returns
        -------
        Optional[dt.AnnotationFile]
            The ``AnnotationFile`` file or ``None`` if the file was not parseable.
        """
        if path.suffix != ".json":
            return None
        return parse_darwin_json(path, 0)
