from typing import Annotated

from fastapi import Query
from pydantic import AliasChoices, AliasGenerator, BaseModel, Field
from pydantic.alias_generators import to_camel


class CamelCaseContract(BaseModel):
    model_config = {
        "alias_generator": AliasGenerator(
            serialization_alias=to_camel,
            validation_alias=lambda field: AliasChoices(to_camel(field), field),
        ),
        "loc_by_alias": False,
    }


class Filter(CamelCaseContract):
    offset: Annotated[int, Field(ge=0)] = 0
    limit: Annotated[int, Field(ge=1, le=20)] = 10


FilterQuery = Annotated[Filter, Query()]
