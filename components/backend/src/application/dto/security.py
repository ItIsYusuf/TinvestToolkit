from pydantic import BaseModel, Field

class UserRegister(BaseModel):
    name: str = Field(
        description='Name'
    )
    surname: str = Field(
        description='Surname'
    )
    patronymic: str = Field(
        description='Patronymic'
    )
    password: str = Field(
        description='Password'
    )
    email: str = Field(
        description='Email',
        pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$',
        default='test@gmail.com'
    )
    token: str = Field(
        description='Invest API Token',
        pattern=r'^t\.[\w-]{86}$'
    )

class UserLogin(BaseModel):
    email: str = Field(
        pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$',
        default='test@gmail.com'
    )
    password: str = Field()