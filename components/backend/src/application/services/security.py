from attr import dataclass

from libs.security import Hasher

from src.application import dto, entities, interfaces

@dataclass
class SecurityService:
    security_repo: interfaces.ISecurityRepo

    async def login_async(self, user: dto.UserLogin) -> entities.Client:
        user_db = await self.security_repo.get_user(user.email)

        if user_db is None:
            raise

        if not Hasher.verify_hash(user.password, user_db.password):
            raise
        return user_db

    async def register_async(self, user: dto.UserRegister) -> None:
        is_exists = await self.security_repo.email_exists(user.email)

        if is_exists:
            raise

        user.password = Hasher.get_hash(user.password)
        await self.security_repo.register_async(user)