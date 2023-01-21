from fastapi import APIRouter
from src.models.database import get_session
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from src.models.schemas import MenuCreate

from src.models.models import menu, submenu, dish, Submenu, Menu


router = APIRouter(
    prefix="/api/v1/menus",
    tags=["submenu"]
)


@router.get("/{api_test_menu_id}/submenus/")
def get_submenu(api_test_menu_id: str, session: Session = Depends(get_session)):
    query = select(submenu).filter(api_test_menu_id == submenu.c.menu_id)
    result = session.execute(query)
    full = result.all()
    return full


@router.get("/{api_test_menu_id}/submenus/{api_test_submenu_id}/")
def get_submenu_id(api_test_menu_id: str, api_test_submenu_id: str, session: Session = Depends(get_session)):
    query = select(submenu).filter(api_test_menu_id == submenu.c.menu_id).filter(
        api_test_submenu_id == submenu.c.id)
    result = session.execute(query)

    full = result.all()
    if full == []:
        raise HTTPException(status_code=404, detail="submenu not found")
    print(full)
    return {"id": full[0].id, "title": full[0].title, "description": full[0].description, "dishes_count": full[0].dishes_count}


@router.post("/{api_test_menu_id}/submenus/", status_code=201)
def create_menu(api_test_menu_id: str, new_submenu: MenuCreate, session: Session = Depends(get_session)):

    stmt = insert(submenu).values(**new_submenu.dict())
    session.execute(stmt)

    add = update(menu).values(submenus_count=menu.c.submenus_count +
                              1).filter(menu.c.id == api_test_menu_id)
    session.execute(add)
    query = select(submenu)
    res = session.execute(query)
    r = res.all()

    update_menu_id = update(submenu).values(
        menu_id=menu.c.id).filter(menu.c.id == api_test_menu_id)
    session.execute(update_menu_id)
    session.commit()
    return {"id": r[0].id, "title": new_submenu.title, "description": new_submenu.description}


@router.patch("/{api_test_menu_id}/submenus/{api_test_submenu_id}/")
def update_submenu(api_test_menu_id: str, api_test_submenu_id: str, item: MenuCreate, session: Session = Depends(get_session)):
    update = session.query(Submenu).filter(
        Submenu.id == api_test_submenu_id, Submenu.menu_id == api_test_menu_id).one_or_none()
    if not update:
        raise HTTPException(status_code=404, detail="submenu not found")
    for var, value in vars(item).items():
        setattr(update, var, value)
    session.commit()

    query = select(submenu).filter(api_test_menu_id == submenu.c.menu_id).filter(
        api_test_submenu_id == submenu.c.id)
    result = session.execute(query)

    full = result.all()
    return {"title": full[0].title, "description": full[0].description}


@router.delete("/{api_test_menu_id}/submenus/{api_test_submenu_id}/",  status_code=200)
def delete_submenu(api_test_menu_id: str, api_test_submenu_id: str, session: Session = Depends(get_session)):
    res = session.query(submenu).filter(
        submenu.c.id == api_test_submenu_id).all()
    count_dish = res[0].dishes_count

    doun_submenus_count = update(menu).values(
        submenus_count=menu.c.submenus_count - 1).filter(menu.c.id == api_test_menu_id)
    doun_dishes_count = update(menu).values(
        dishes_count=menu.c.dishes_count - count_dish).filter(menu.c.id == api_test_menu_id)

    session.query(dish).filter(api_test_menu_id == submenu.c.menu_id,
                               submenu.c.id == dish.c.submenu_id).delete()
    session.query(submenu).filter(submenu.c.id == api_test_submenu_id).delete()
    session.execute(doun_submenus_count)
    session.execute(doun_dishes_count)

    session.commit()
    return {"status": True, "message": "The dish has been deleted"}
