import uvicorn
from fastapi import Depends
from fastapi import FastAPI, Response, status
from sqlalchemy import select

from models import get_session
from models.db_models import Categories
from models.schema_models import CategoriesCreate

app = FastAPI()


@app.post("/create-category/")
async def create_category(data: CategoriesCreate, response: Response, db_session=Depends(get_session)):
    try:
        async with db_session as session:
            db_obj = Categories(title=data.title)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
        return {"data": db_obj, "status": True, "message": "category created"}

    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return {"data": {}, "status": False, "message": "error while creating category"}


@app.post("/categories/")
async def get_categories(response: Response, db_session=Depends(get_session)):
    try:
        async with db_session as session:
            categories = (await session.scalars(select(Categories).where(Categories.is_deleted == False))).all()
        return {"data": categories, "status": True, "message": "category list fetched"}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return {"data": [], "status": False, "message": "error while fetching category"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
