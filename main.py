# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Path, Form

app = FastAPI()

# Models


class LoginOut(BaseModel):
    username: str = Field(
        ...,
        title="Username",
        max_length=20,
        example="jusart"
    )
    message: str = Field(
        default="Login successful")


class HeirColor(Enum):
    white = "white"
    brown = "brown",
    black = "black",
    blonde = "blonde",
    red = "red",


class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    contry: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Arturo",
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Juarez",
    )

    email: EmailStr = Field(..., example="jusart.92@gmail.com")
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=25,
    )
    hair_color: Optional[HeirColor] = Field(
        default=None)
    is_married: Optional[bool] = Field(
        default=None,
    )
    password: str = Field(..., min_length=8)


@ app.get(path="/", status_code=status.HTTP_200_OK)
def home():
    return {"message": "Hello World!"}


@ app.post(
    path="/person/new",
    response_model=Person,
    response_model_exclude={"password"},
    status_code=status.HTTP_201_CREATED,
)
def create_person(person: Person = Body(...)):
    return person


@ app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
)
def show_person(
    name: Optional[str] = Query(
        None, min_length=1,
        max_length=50,
        title="Person Name",
        description="This is ther person name. It's between 1 and 50 characters",
        example="John Doe",
    ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's require",
        example=25,
    )
):
    return {"name": name, "age": age}

# Validaciones: Path Parameters


@ app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=123,
    )
):
    return {person_id: "It exist!"}

# Validaciones: Request Body


@ app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123,
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results


@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
)
def login(
    username: str = Form(...),
    password: str = Form(...),
):
    return LoginOut(username=username)
