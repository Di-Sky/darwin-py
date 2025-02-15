from darwin.datatypes import ImportParser

from .importer import import_annotations  # noqa

from importlib.metadata import entry_points

class ImporterNotFoundError(ModuleNotFoundError):
    pass


def get_importer(format: str) -> ImportParser:
    parsers = entry_points(group="darwin-import-parsers")
    if format not in parsers.names:
        raise ImporterNotFoundError(f"Unsupported import format: {format}, currently supported: {parsers.names}")
    return parsers[format].load()
