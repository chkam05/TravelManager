from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List

from core.data.base_data_model import BaseDataModel
from models.settings.favourite_place import FavouritePlace
from models.settings.favourite_tag import FavouriteTag


@dataclass
class FavouritesTransferDataModel(BaseDataModel):
    """Stores the explicit favourites and tags transfer payload."""

    # Default values

    # Field name declarations
    FIELD_FAVOURITE_TAGS: ClassVar[str] = 'favourite_tags'
    FIELD_FAVOURITES: ClassVar[str] = 'favourites'

    # Fields
    favourite_tags: List[FavouriteTag]
    favourites: List[FavouritePlace]

    #region Serialization

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> FavouritesTransferDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        tags = d.get(cls.FIELD_FAVOURITE_TAGS, [])
        favourites = d.get(cls.FIELD_FAVOURITES, [])
        return cls(
            favourite_tags=FavouriteTag.from_dict_list(tags if isinstance(tags, list) else []),
            favourites=FavouritePlace.from_dict_list(
                favourites if isinstance(favourites, list) else []
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.FIELD_FAVOURITE_TAGS: self.to_dict_list(self.favourite_tags),
            self.FIELD_FAVOURITES: self.to_dict_list(self.favourites)
        }

    #endregion Serialization
