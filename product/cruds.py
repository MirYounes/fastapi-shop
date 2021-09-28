from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import aiofiles
from . import models


def get_products(db: Session, skip, limit):
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_product_by_id(db: Session, id: int):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')
    return product


async def create(
    db: Session,
    title,
    description,
    image,
    price,
    galleries
    ):
    image_path = f'media/products/{image.filename}'
    async with aiofiles.open(image_path, 'wb') as out_file:
        content = await image.read()  # async read
        await out_file.write(content)  # async write

    product = models.Product(
        title=title,
        description=description,
        image=image_path,
        price=price
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    await create_gallery(db, galleries, product.id)
    return product


async def create_gallery(db, galleries, product_id):
    for image in galleries:
        image_path = f'media/galleries/{image.filename}'
        async with aiofiles.open(image_path, 'wb') as out_file:
            content = await image.read()  # async read
            await out_file.write(content)  # async write
        gallery = models.Gallery(product_id=product_id, image=image_path)
        db.add(gallery)
        db.commit()
        db.refresh(gallery)


async def update(
    id,
    db,
    title,
    description,
    price,
    available,
    image
    ):
    product = db.query(models.Product).filter(models.Product.id == id).one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")
    
    image_path = None
    if image :
        image_path = f'media/products/{image.filename}'
        async with aiofiles.open(image_path, 'wb') as out_file:
            content = await image.read()  # async read
            await out_file.write(content)  # async write

    product.title = title or product.title
    product.price = price or product.price
    product.description = description or product.description
    if available !=None:
        product.available = available
    product.image = image_path or product.image


    db.commit()
    db.refresh(product)
    return product



def delete_product(id:int,db: Session):
    product = db.query(models.Product).filter(models.Product.id == id).one_or_none()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")

    #product.delete(synchronize_session=False)
    db.delete(product)
    db.commit()
