from typing import cast

from sqlalchemy import update
from sqlalchemy.engine import BaseCursorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from argstore.parameters import models, schemas

_possible_types = {"str": str, "int": int}


def _cast_database_parameter_to_schema(param: models.Parameter) -> schemas.Parameter:
    return schemas.Parameter(
        id=param.id,
        name=param.name,
        value=_possible_types[str(param.type)](param.value),
    )


def map_param_from_schema_to_model_dict(param: schemas.CreateParameter) -> dict:
    return dict(
        name=param.name, type=type(param.value).__name__, value=str(param.value)
    )


async def create_parameter(
    db: AsyncSession, param: schemas.CreateParameter
) -> models.Parameter:
    db_param = models.Parameter(**map_param_from_schema_to_model_dict(param))
    db.add(db_param)
    await db.commit()
    await db.refresh(db_param)
    return db_param


async def read_parameter(db: AsyncSession, param_id: int) -> models.Parameter | None:
    return (
        (
            await db.execute(
                select(models.Parameter).where(models.Parameter.id == param_id)
            )
        )
        .scalars()
        .first()
    )


async def read_parameters(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[models.Parameter]:
    return (
        (await db.execute(select(models.Parameter).offset(skip).limit(limit)))
        .scalars()
        .all()
    )


async def update_parameter(
    db: AsyncSession, param: schemas.Parameter
) -> models.Parameter | None:
    # param_to_update = await read_parameter(db, param.id)

    query = (
        update(models.Parameter)
        .where(models.Parameter.id == param.id)
        .values(map_param_from_schema_to_model_dict(param))
        .execution_options(synchronize_session="fetch")
    )

    update_result = cast(BaseCursorResult, await db.execute(query))
    if cast(int, update_result.rowcount) > 0:
        await db.commit()
        return await read_parameter(db, param.id)
    return None


async def delete_parameter(db: AsyncSession, param_id: int) -> bool:
    if to_del := await read_parameter(db, param_id):
        await db.delete(to_del)
        await db.commit()
        return True
    return False
