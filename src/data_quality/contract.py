"""The data contract: what counts as acceptable input.

Every rule lives here, so changing the contract never means
hunting through the codebase.
"""
from dataclasses import dataclass


@dataclass
class Contract:
    """Rules every input file must satisfy."""
    required_columns: tuple[str, ...] = ("id", "birthdate", "gender")
    unique_key: str = "id"
    date_columns: tuple[str, ...] = ("birthdate", "deathdate")
    date_format: str = "%Y-%m-%d"


DEFAULT_CONTRACT = Contract()

