from fastapi import APIRouter
from models.database import get_session
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from models.schemas import DishCreate

from models.models import menu, submenu, dish, Dish


router = APIRouter(
    prefix="/api/v1/menus",
    tags=["dish"]
)


@router.get("/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/")
def get_dish(api_test_menu_id: str, api_test_submenu_id: str, session: Session = Depends(get_session)):
    query = select(dish).join(submenu).filter(
        api_test_submenu_id == dish.c.submenu_id)
    result = session.execute(query)
    full = result.all()

    return full


@router.get("/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}/")
def get_dish_id(api_test_menu_id: str, api_test_submenu_id: str, api_test_dish_id: str, session: Session = Depends(get_session)):
    query = select(dish).join(submenu).filter(
        api_test_submenu_id == dish.c.submenu_id, api_test_dish_id == dish.c.id)
    result = session.execute(query)
    full = result.all()

    if not full:
        raise HTTPException(status_code=404, detail="dish not found")
    return {"id": full[0].id, "title": full[0].title, "description": full[0].description, "price": full[0].price}


@router.post("/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/",  status_code=201)
def create_dish(api_test_menu_id: str, api_test_submenu_id: str, new_dish: DishCreate, session: Session = Depends(get_session)):
    stmt = insert(dish).values(**new_dish.dict())
    session.execute(stmt)

    # update count
    add_count_dish = update(menu).values(
        dishes_count=menu.c.dishes_count + 1).filter(menu.c.id == api_test_menu_id)
    session.execute(add_count_dish)

    add_count_dish_submenu = update(submenu).values(
        dishes_count=submenu.c.dishes_count + 1).filter(submenu.c.id == api_test_submenu_id)
    session.execute(add_count_dish_submenu)

    query = select(dish)
    res = session.execute(query)
    r = res.all()

    update_dish_id = update(dish).values(submenu_id=submenu.c.id).filter(
        menu.c.id == api_test_menu_id, submenu.c.id == api_test_submenu_id)
    session.execute(update_dish_id)

    session.commit()
    return {"id": r[0].id, "title": new_dish.title, "description": new_dish.description, "price": new_dish.price}


@router.patch("/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}/")
def update_dish(api_test_menu_id: str, api_test_submenu_id: str, api_test_dish_id: str,  item: DishCreate, session: Session = Depends(get_session)):
    update = session.query(Dish).filter(
        Dish.id == api_test_dish_id, Dish.submenu_id == api_test_submenu_id).one_or_none()
    if not update:
        raise HTTPException(status_code=404, detail="menu not found")
    for var, value in vars(item).items():
        setattr(update, var, value)
    session.commit()

    query = select(dish).filter(api_test_menu_id == submenu.c.menu_id).filter(
        api_test_submenu_id == submenu.c.id).filter(api_test_dish_id == dish.c.id)
    result = session.execute(query)
    full = result.all()
    return {"title": full[0].title, "description": full[0].description, "price": full[0].price}


@router.delete("/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}/")
def delete_dish(api_test_menu_id: str, api_test_submenu_id: str, api_test_dish_id: str, session: Session = Depends(get_session)):
    session.query(dish).filter(
        dish.c.id == api_test_dish_id).delete()

    # update count
    doun_count_dish = update(menu).values(
        dishes_count=menu.c.dishes_count - 1).filter(menu.c.id == api_test_menu_id)
    session.execute(doun_count_dish)
    doun_count_dish_submenu = update(submenu).values(
        dishes_count=submenu.c.dishes_count - 1).filter(submenu.c.id == api_test_submenu_id)
    session.execute(doun_count_dish_submenu)

    session.commit()
    return {"status": True, "message": "The dish has been deleted"}
