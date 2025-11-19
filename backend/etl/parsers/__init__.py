"""
Factor data parsers for different sources.
"""
from .ken_french import KenFrenchParser
from .generic_csv import GenericCSVParser

# Parser registry
PARSERS = {
    'ken_french': KenFrenchParser,
    'generic_csv': GenericCSVParser,
}


def get_parser(parser_name: str):
    """Get parser class by name."""
    if parser_name not in PARSERS:
        raise ValueError(f"Unknown parser: {parser_name}")
    return PARSERS[parser_name]
