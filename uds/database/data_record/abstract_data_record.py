"""Definition of AbstractDataRecord which is a base class for all Data Records."""

__all__ = ["AbstractDataRecord", "DataRecordPhysicalValueAlias", "DecodedDataRecord"]

from abc import ABC, abstractmethod
from typing import Optional, Tuple, TypedDict, Union

DataRecordPhysicalValueAlias = Union[int, float, str, Tuple["DecodedDataRecord", ...]]
"""Alias of Data Records' physical value."""


class DecodedDataRecord(TypedDict):
    """Structure of decoded Data Record."""

    name: str
    raw_value: int
    physical_value: DataRecordPhysicalValueAlias  # noqa: F841


class AbstractDataRecord(ABC):
    """Common implementation and interface for all Data Records."""

    def __init__(self, name: str) -> None:
        """
        Initialize common part for all Data Records.

        :param name: Name to assign to this Data Record.

        :raise TypeError: Provided value of name is not str type.
        """
        if not isinstance(name, str):
            raise TypeError("Provided name is not str type.")
        self.__name = name.strip()

    @property
    def name(self) -> str:
        """Name of this Data Record."""
        return self.__name

    @property  # noqa: F841
    @abstractmethod
    def length(self) -> int:
        """Get number of bits that this Data Record is stored over."""

    @property
    def max_raw_value(self):
        """
        Maximum raw (bit) value for this Data Record.

        :return: Maximum value that can be represented by `length` bits.
        """
        return (1 << self.length) - 1

    @property  # noqa: F841
    @abstractmethod
    def is_reoccurring(self) -> bool:
        """
        Whether this Data Record might occur multiple times.

        Values meaning:
        - False - exactly one occurrence in every diagnostic message
        - True - number of occurrences might vary
        """

    @property  # noqa: F841
    @abstractmethod
    def min_occurrences(self) -> int:
        """
        Minimal number of this Data Record occurrences.

        .. note:: Relevant only if :attr:`~uds.database.abstract_data_record.AbstractDataRecord.is_reoccurring`
            equals True.
        """

    @property  # noqa: F841
    @abstractmethod
    def max_occurrences(self) -> Optional[int]:
        """
        Maximal number of this Data Record occurrences.

        .. note:: Relevant only if :attr:`~uds.database.abstract_data_record.AbstractDataRecord.is_reoccurring`
            equals True.
        .. warning:: No maximal number (infinite number of occurrences) is represented by None value.
        """

    @property  # noqa: F841
    @abstractmethod
    def contains(self) -> Tuple["AbstractDataRecord", ...]:
        """Get Data Records contained by this Data Record."""

    @abstractmethod
    def decode(self, raw_value: int) -> DecodedDataRecord:  # noqa: F841
        """
        Decode physical value for provided raw value.

        :param raw_value: Raw (bit) value of Data Record.

        :return: Dictionary with physical value for this Data Record.
        """

    @abstractmethod
    def encode(self, physical_value: DataRecordPhysicalValueAlias) -> int:  # noqa: F841
        """
        Encode raw value for provided physical value.

        :param physical_value: Physical (meaningful e.g. float, str type) value of this Data Record.

        :return: Raw Value of this Data Record.
        """
