import asyncio

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.user import User, Role
from app.core.security import hash_password


async def create_admin():
    nome = "Admin Ing"
    email = "admining@upath.com"
    senha = "SenhaForte123!"

    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.email == email.lower())
        )
        existing = result.scalar_one_or_none()

        if existing:
            print(f"Já existe um usuário com o e-mail {email}")
            print(f"ID: {existing.id} | role: {existing.role}")
            return

        user = User(
            nome=nome,
            email=email.lower(),
            senha_hash=hash_password(senha),
            role=Role.admin,
            is_active=True,
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        print("Usuário admin criado com sucesso!")
        print(f"ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")


if __name__ == "__main__":
    asyncio.run(create_admin())
