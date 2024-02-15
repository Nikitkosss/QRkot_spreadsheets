from datetime import datetime
from typing import List, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject, Donation


async def get_not_invested_objects(
    model_in: Union[CharityProject, Donation],
    session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    db_objects = await charity_project_crud.get_db_objects(model_in, session)
    return db_objects.scalars().all()


async def close_invested_object(
    obj_to_close: Union[CharityProject, Donation]
) -> None:
    obj_to_close.fully_invested = True
    obj_to_close.close_date = datetime.now()


async def execute_investment_process(
    object_in: Union[CharityProject, Donation],
    session: AsyncSession
):
    db_model = CharityProject if isinstance(object_in, Donation) else Donation
    not_invested_objects = await get_not_invested_objects(db_model, session)
    available_amount = object_in.full_amount

    for not_invested_obj in not_invested_objects:
        need_to_invest = (not_invested_obj.full_amount -
                          not_invested_obj.invested_amount)
        to_invest = min(need_to_invest, available_amount)
        not_invested_obj.invested_amount += to_invest
        object_in.invested_amount += to_invest
        available_amount -= to_invest

        if not_invested_obj.full_amount == not_invested_obj.invested_amount:
            await close_invested_object(not_invested_obj)

        if not available_amount:
            await close_invested_object(object_in)
            break

    await session.commit()

    return object_in
