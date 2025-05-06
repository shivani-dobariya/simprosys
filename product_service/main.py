import uvicorn
from fastapi import Depends
from fastapi import FastAPI, Response, status
from sqlalchemy import select

from models import get_session
from models.db_models import Products
from models.schema_models import ProductsCreate, ProductsUpdate, ProductsID

app = FastAPI()


@app.post("/create-products/")
async def create_products(data: ProductsCreate, response: Response, db_session=Depends(get_session)):
    try:
        async with db_session as session:
            db_obj = Products(title=data.title, category_id=data.category_id, description=data.description,
                              price=data.price)
            session.add(db_obj)
            session.commit()
        return {"data": db_obj, "status": True, "message": "products created"}

    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return {"data": {}, "status": False, "message": "error while creating products"}


@app.post("/products/")
async def get_products(response: Response, db_session=Depends(get_session)):
    try:
        async with db_session as session:
            products = (await session.scalars(select(Products).where(Products.is_deleted == False))).all()
        return {"data": products, "status": True, "message": "products list fetched"}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return {"data": [], "status": False, "message": "error while fetching products"}


@app.post("/update-product/")
async def get_products(data: ProductsUpdate, response: Response, db_session=Depends(get_session)):
    try:
        async with db_session as session:
            existing_product = (await session.scalars(
                select(Products).where(Products.id == data.id, Products.is_deleted == False))).first()
            if existing_product:
                existing_product.title = data.title
                existing_product.category_id = data.category_id
                existing_product.description = data.description
                existing_product.price = data.price
                session.commit()
                session.refresh(existing_product)
                return {"data": existing_product, "status": True, "message": "products updated"}
            else:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"data": {}, "status": True, "message": "no product found"}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return {"data": [], "status": False, "message": "error while updating products"}


@app.post("/delete-product/")
async def get_products(data: ProductsID, response: Response, db_session=Depends(get_session)):
    try:
        async with db_session as session:
            existing_product = (await session.scalars(
                select(Products).where(Products.id == data.id, Products.is_deleted == False))).first()
            existing_product.is_deleted = True
            session.commit()
        return {"data": {}, "status": True, "message": "products deleted"}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return {"data": [], "status": False, "message": "error while deleting products"}


@app.post("/product-detail/")
async def get_products(data: ProductsID, response: Response, db_session=Depends(get_session)):
    try:
        async with db_session as session:
            existing_product = (await session.scalars(
                select(Products).where(Products.id == data.id, Products.is_deleted == False))).first()
        if existing_product:
            return {"data": existing_product or {}, "status": True, "message": "products fetched"}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"data": {}, "status": True, "message": "no product found"}

    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return {"data": [], "status": False, "message": "error while fetching product detail"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
