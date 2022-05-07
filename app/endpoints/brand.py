"""Router for brand."""
from typing import Any

from fastapi import APIRouter, Depends

from .. import exceptions as exc
from ..crud.brand import CRUDBrand
from ..deps import get_current_user
from ..models.user import User as UserModel
from ..schemas.brand import Brand, BrandCreate, BrandUpdate
from ..schemas.message import Message

router = APIRouter()


@router.get(
    "",
    response_model=list[Brand]
)
async def get_brands(
    current_user: UserModel = Depends(get_current_user)
) -> Any:
    """Get all brands that belong to current user."""
    return await CRUDBrand.get_multi(user_obj=current_user)


@router.post(
    "",
    status_code=201,
    response_model=Brand
)
async def create_brand(
    brand_in: BrandCreate,
    current_user: UserModel = Depends(get_current_user)
) -> Any:
    """
    ## Add new brand

    required
    - **name**: name of brand

    optional
    - **about**: introduction of brand
    - **social_media**: brand's social media
    - **website**: brand's website
    - **email**: brand's email
    - **phone**: brand's phone number

    notes
    - Each brand must contain at least one contact info.
    """
    brand = await CRUDBrand.get_by_name(
        name=brand_in.name, user_obj=current_user)
    if brand:
        raise exc.ConflictError("Brand already exists")
    return await CRUDBrand.create(user_obj=current_user, obj_in=brand_in)


@router.patch(
    "/{brand_id}",
    response_model=Brand
)
async def update_brand(
    brand_id: str,
    brand_in: BrandUpdate,
    current_user: UserModel = Depends(get_current_user)
) -> Any:
    """
    ## Update brand

    optional
    - **about**: introduction of brand
    - **social_media**: brand's social media
    - **website**: brand's website
    - **email**: brand's email
    - **phone**: brand's phone number
    - **is_active**: default to true
    """
    brand = await CRUDBrand.get_by_id(
        brand_id=brand_id, user_obj=current_user)
    if brand is None:
        raise exc.NotFoundError("Brand not found")
    return await CRUDBrand.update(brand_obj=brand, obj_in=brand_in)


@router.delete(
    "/{brand_id}",
    response_model=Message,
)
async def delete_brand(
    brand_id: str,
    current_user: UserModel = Depends(get_current_user)
) -> Any:
    """Delete the brand that belong to current user."""
    brand = await CRUDBrand.get_by_id(
        brand_id=brand_id, user_obj=current_user)
    if brand is None:
        raise exc.NotFoundError("Brand not found")
    removed_brand = await CRUDBrand.remove(brand_obj=brand)
    return Message(message=f"Deleted brand: {removed_brand.name}")
