"""CRUD for brand."""
from ..models.brand import Brand as BrandModel
from ..models.user import User as UserModel
from ..schemas.brand import BrandCreate, BrandUpdate


class CRUDBrand:

    @classmethod
    async def get_all(
        cls, *, user_obj: UserModel
    ) -> list[BrandModel]:
        """Get all brands that belong to current user."""
        return (
            await BrandModel.objects
            .filter(BrandModel.owner.email == user_obj.email)
            .order_by(BrandModel.created_time.desc())
            .all()
        )

    @classmethod
    async def get_by_id(
        cls, *, brand_id: str, user_obj: UserModel | None = None
    ) -> BrandModel | None:
        """Get the brand by brand id that belong to current user."""
        brand_obj = (
            BrandModel.objects.select_related("products")
            .filter(BrandModel.id == brand_id)
        )
        if user_obj:
            brand_obj = brand_obj.filter(BrandModel.owner.email == user_obj.email)  # noqa: E501
        return await brand_obj.get_or_none()

    @classmethod
    async def get_by_name(
        cls, *, name: str, user_obj: UserModel
    ) -> BrandModel | None:
        """Get the brand by brand name that belong to current user."""
        return (
            await BrandModel.objects
            .filter(BrandModel.name == name)
            .filter(BrandModel.owner.email == user_obj.email)
            .get_or_none()
        )

    @classmethod
    async def create(
        cls, *, user_obj: UserModel, obj_in: BrandCreate
    ) -> BrandModel:
        """Create the brand by current user."""
        return await BrandModel.objects.create(**obj_in.dict(), owner=user_obj)

    @classmethod
    async def update(
        cls, *, brand_obj: BrandModel, obj_in: BrandUpdate
    ) -> BrandModel:
        """Update the brand."""
        return await brand_obj.update(**obj_in.dict(exclude_unset=True))

    @classmethod
    async def remove(
        cls, *, brand_obj: BrandModel
    ) -> BrandModel:
        """Delete the brand."""
        await brand_obj.delete()
        return brand_obj

    @staticmethod
    def is_active(brand: BrandModel) -> bool:
        """Check if brand is active."""
        return brand.is_active
