from http import HTTPStatus

from fastapi import HTTPException
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject

NOT_FOUND_ERROR = 'Данный проект не найден!'
EXISTS_ERROR = 'Проект с таким именем уже существует!'
UPDATE_ERROR = 'Закрытый проект нельзя редактировать!'
DELETION_ERROR = 'В проект были внесены средства, не подлежит удалению!'
AMOUNT_ERROR = 'Новая требуемая сумма должна быть больше уже внесенной.'


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession
) -> None:
    charity_project_id = await charity_project_crud.get_project_id_by_name(
        project_name=project_name,
        session=session
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=EXISTS_ERROR
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get_charity_project(
        object_id=project_id,
        session=session
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=NOT_FOUND_ERROR
        )
    return charity_project


async def check_project_was_closed(
    project_id: int,
    session: AsyncSession
):
    project_close_date = await charity_project_crud.get_charity_project_close_date(
        project_id,
        session
    )
    if project_close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=UPDATE_ERROR
        )


async def check_project_was_invested(
    project_id: int,
    session: AsyncSession
):
    invested_project = await charity_project_crud.get_charity_project_invested_amount(
        project_id,
        session
    )
    if invested_project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=DELETION_ERROR
        )


async def check_correct_full_amount_for_update(
    project_id: int,
    session: AsyncSession,
    full_amount_to_update: PositiveInt
):
    db_project_invested_amount = await charity_project_crud.get_charity_project_invested_amount(
        project_id,
        session
    )
    if db_project_invested_amount > full_amount_to_update:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=AMOUNT_ERROR
        )