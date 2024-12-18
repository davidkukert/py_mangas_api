import uuid
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from mangas_api.db import T_Session
from mangas_api.models import User
from mangas_api.schemas import (
    Message,
    UserCreate,
    UserDetails,
    UserList,
    UserUpdate,
)
from mangas_api.security import get_password_hash

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.get('/', response_model=UserList)
async def read_users(session: T_Session):
    users_list = await session.scalars(select(User))
    return {'users': users_list}


@router.get('/{user_id}', response_model=UserDetails)
async def read_user(user_id: uuid.UUID, session: T_Session):
    user_details = await session.scalar(select(User).where(User.id == user_id))

    if user_details is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return {'user': user_details}


@router.post('/', response_model=UserDetails)
async def create_user(user: UserCreate, session: T_Session):
    db_user = await session.scalar(
        select(User).where(User.username == user.username)
    )
    if db_user is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Username already taken'
        )

    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return {'user': db_user}


@router.put('/{user_id}', response_model=UserDetails)
async def update_user(
    user_id: uuid.UUID, user: UserUpdate, session: T_Session
):
    db_user = await session.scalar(select(User).where(User.id == user_id))

    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    db_user_conflict = await session.scalar(
        select(User).where(
            (User.username == user.username) & (User.id != user_id)
        )
    )

    if db_user_conflict is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Username already taken'
        )

    if user.username is not None:
        db_user.username = user.username

    if user.password is not None:
        db_user.password = get_password_hash(user.password)

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return {'user': db_user}


@router.delete('/{user_id}', response_model=Message)
async def delete_user(user_id: uuid.UUID, session: T_Session):
    db_user = await session.scalar(select(User).where(User.id == user_id))

    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    await session.delete(db_user)
    await session.commit()

    return {'message': 'Usuário deletado!'}
