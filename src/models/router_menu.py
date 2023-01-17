from fastapi import APIRouter
from models.database import get_session
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from models.schemas import MenuCreate


from models.models import menu, submenu, dish, Menu

router = APIRouter(
    prefix="/api/v1/menus",
    tags=["menu"]
)


@router.get("/")
def get_menu(session: Session = Depends(get_session)):
    query = select(menu)
    result = session.execute(query)
    return result.all()


@router.get("/{target_menu_id}/", status_code=200)
def get_menu_id(target_menu_id: str, session: Session = Depends(get_session)):

    query = select(menu).where(menu.c.id == target_menu_id)
    result = session.execute(query)
    full = result.all()
    if not full:
        raise HTTPException(status_code=404, detail="menu not found")

    return {"id": full[0].id, "title": full[0].title, "description": full[0].description, "submenus_count": full[0].submenus_count, "dishes_count": full[0].dishes_count}


@router.post("/", status_code=201)
def create_menu(new_menu: MenuCreate, session: Session = Depends(get_session)):

    stmt = insert(menu).values(**new_menu.dict())
    session.execute(stmt)
    session.commit()

    query = select(menu)
    res = session.execute(query)
    r = res.all()
    print(r[0].id)
    return {"id": r[0].id, "title": new_menu.title, "description": new_menu.description}


@router.patch("/{api_test_menu_id}/")
def update_menu(api_test_menu_id: str, item: MenuCreate, session: Session = Depends(get_session)):
    update = session.query(Menu).filter(
        Menu.id == api_test_menu_id).one_or_none()

    if not update:
        raise HTTPException(status_code=404, detail="menu not found")
    for var, value in vars(item).items():
        setattr(update, var, value)
    session.commit()

    return get_menu_id(api_test_menu_id, session)


@router.delete("/{api_test_menu_id}/")
def delete_menu(api_test_menu_id: str, session: Session = Depends(get_session)):

    session.query(dish).filter(api_test_menu_id == submenu.c.menu_id,
                               submenu.c.id == dish.c.submenu_id).delete()
    session.query(submenu).filter(api_test_menu_id == menu.c.id,
                                  menu.c.id == submenu.c.menu_id).delete()
    session.query(menu).filter(menu.c.id == api_test_menu_id).delete()
    session.commit()

    return {"status": True, "message": "The dish has been deleted"}
