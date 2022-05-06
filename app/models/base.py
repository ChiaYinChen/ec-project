"""Base model."""
import ormar

from ..db.session import database, metadata


class BaseMeta(ormar.ModelMeta):

    metadata = metadata
    database = database
