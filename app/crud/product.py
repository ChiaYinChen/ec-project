"""CRUD for product."""
from fastapi import UploadFile

from ..models.brand import Brand as BrandModel
from ..models.product import Product as ProductModel
from ..schemas.product import ProductCreate, ProductUpdate


class CRUDProduct:

    @classmethod
    async def get_all(
        cls, *, brand_id: str
    ) -> list[ProductModel]:
        """Get all products for that brand."""
        return (
            await ProductModel.objects.select_related("brand")
            .filter(ProductModel.brand.id == brand_id)
            .order_by(ProductModel.created_time.desc())
            .all()
        )

    @classmethod
    async def get_by_title(
        cls, *, title: str, brand_obj: BrandModel
    ) -> ProductModel | None:
        """Get a product for that brand by product title."""
        return (
            await ProductModel.objects.select_related("brand")
            .filter(ProductModel.title == title)
            .filter(ProductModel.brand.id == brand_obj.id)
            .get_or_none()
        )

    @classmethod
    async def create(
        cls,
        *,
        brand_obj: BrandModel,
        img_obj: UploadFile | None = None,
        obj_in: ProductCreate
    ) -> ProductModel:
        """Create a product for that brand."""
        content = await img_obj.read() if img_obj else None
        return await ProductModel.objects.create(
            **obj_in.dict(), image=content, brand=brand_obj)

    @classmethod
    async def update(
        cls,
        *,
        product_obj: ProductModel,
        obj_in: ProductUpdate
    ) -> ProductModel:
        """Update a product."""
        return await product_obj.update(**obj_in.dict(exclude_unset=True))

    @classmethod
    async def remove(
        cls, *, product_obj: ProductModel
    ) -> ProductModel:
        """Delete a product."""
        await product_obj.delete()
        return product_obj
