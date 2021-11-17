# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models


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

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "John",
    #             "last_name": "Doe",
    #             "email": "jusart.92@gmail.com",
    #             "age": 25,
    #             "hair_color": "brown",
    #             "is_married": True,
    #         }
    #     }


@ app.get("/")
def home():
    return {"message": "Hello World!"}


@ app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person


@ app.get("/person/detail")
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
