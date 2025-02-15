from importlib import import_module

from darwin.datatypes import ImportParser

from .importer import import_annotations  # noqa

from .formats import supported_formats

class ImporterNotFoundError(ModuleNotFoundError):
    pass


def get_importer(format: str) -> ImportParser:
    if format not in supported_formats:
        raise ImporterNotFoundError(f"Unsupported import format: {format}, currently supported: {supported_formats}")
    module = import_module(f"darwin.importer.formats.{format}")
    return getattr(module, "parse_path")
