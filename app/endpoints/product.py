"""Router for product."""
from typing import Any

from fastapi import APIRouter, Depends, File, Path, Query, UploadFile

from .. import exceptions as exc
from ..crud.brand import CRUDBrand
from ..crud.product import CRUDProduct
from ..deps import (get_active_brand, get_current_user,
                    get_current_user_optional)
from ..models.brand import Brand as BrandModel
from ..models.user import User as UserModel
from ..schemas.message import Message
from ..schemas.product import Product, ProductCreate, ProductUpdate

router = APIRouter()


@router.get(
    "/{brand_id}/products",
    response_model=list[Product],
    summary="Get Products (login optional)",
)
async def get_products(
    brand_id: str = Path(...),
    current_user: UserModel | None = Depends(get_current_user_optional),
    current_brand: BrandModel | None = Depends(get_active_brand)
) -> Any:
    """
    Get all products for that brand.

    notes
    - When the brand is not active, only user with
      an access token can access endpoint.
    """
    if current_user is None and current_brand is None:
        raise exc.UnauthorizedError(message="Inactive brand")
    if current_user and current_brand is None:
        brand = await CRUDBrand.get_by_id(
            brand_id=brand_id, user_obj=current_user)
        if brand is None:
            raise exc.NotFoundError("Brand not found")
    return await CRUDProduct.get_all(brand_id=brand_id)


@router.post(
    "/{brand_id}/products",
    status_code=201,
    response_model=Product
)
async def create_product(
    brand_id: str = Path(...),
    current_user: UserModel = Depends(get_current_user),
    item: ProductCreate = Depends(ProductCreate.as_form),
    image: UploadFile | None = File(None)
) -> Any:
    """
    ## Add new product

    required
    - **title**: name of product
    - **discount_rate**: the amount of money reduced from the list price
                         expressed as a percentage(float)

    optional
    - **description**: description of product
    - **image**: image of product, it will convert image to base64

    notes
    - User can only edit their own products.
    """
    brand = await CRUDBrand.get_by_id(
        brand_id=brand_id, user_obj=current_user)
    if brand is None:
        raise exc.NotFoundError("Brand not found")
    product = await CRUDProduct.get_by_title(
        title=item.title, brand_obj=brand)
    if product:
        raise exc.ConflictError("Product already exists")
    return await CRUDProduct.create(brand_obj=brand, img_obj=image, obj_in=item)  # noqa: E501


@router.patch(
    "/{brand_id}/products",
    response_model=Product
)
async def update_product(
    item: ProductUpdate,
    brand_id: str = Path(...),
    title: str = Query(..., description="The name of the product to update."),
    current_user: UserModel = Depends(get_current_user),

) -> Any:
    """
    ## Update product

    required
    - **title**: name of product
    - **discount_rate**: the amount of money reduced from the list price
                         expressed as a percentage(float)

    optional
    - **description**: description of product

    notes
    - User can only edit their own products.
    """
    brand = await CRUDBrand.get_by_id(
        brand_id=brand_id, user_obj=current_user)
    if brand is None:
        raise exc.NotFoundError("Brand not found")
    product = await CRUDProduct.get_by_title(
        title=title, brand_obj=brand)
    if product is None:
        raise exc.NotFoundError("Product not found")
    return await CRUDProduct.update(
        product_obj=product, obj_in=item)


@router.delete(
    "/{brand_id}/products",
    response_model=Message,
)
async def delete_product(
    brand_id: str = Path(...),
    title: str = Query(..., description="The name of the product to delete."),
    current_user: UserModel = Depends(get_current_user)
) -> Any:
    """
    Delete a product that belong to current user.

    notes
    - User can only delete their own products.
    """
    brand = await CRUDBrand.get_by_id(
        brand_id=brand_id, user_obj=current_user)
    if brand is None:
        raise exc.NotFoundError("Brand not found")
    product = await CRUDProduct.get_by_title(
        title=title, brand_obj=brand)
    if product is None:
        raise exc.NotFoundError("Product not found")
    removed_product = await CRUDProduct.remove(product_obj=product)
    return Message(message=f"Deleted product: {removed_product.title}")
