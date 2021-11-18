# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# FastAPI
from fastapi import FastAPI, params
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, File, UploadFile

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


@ app.get(path="/", status_code=status.HTTP_200_OK, tags=["Home"])
def home():
    return {"message": "Hello World!"}


@ app.post(
    path="/person/new",
    response_model=Person,
    response_model_exclude={"password"},
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create a new person",
)
def create_person(person: Person = Body(...)):
    """
    Create Person

    This path operation creates a new person in the appp anda save the information
    in the database.

    Parameters:
    - Request body parameters (JSON):
        - **person: Person** -> A person model with first_name, last_name, email, age, hair_color, is_married and password.

    Returns a person model with the information of the new person.
    """
    return person


@ app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    deprecated=True,
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
person = [1, 2, 3, 4, 5]


@ app.get("/person/detail/{person_id}", tags=["Persons"],)
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=123,
    )
):
    if person_id not in person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found"
        )
    return {person_id: "It exist!"}

# Validaciones: Request Body


@ app.put("/person/{person_id}", tags=["Persons"])
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

# Forms


@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def login(
    username: str = Form(...),
    password: str = Form(...),
):
    return LoginOut(username=username)

# Cookies and Headers Parameters


@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Home"],
)
def contact(
    first_name: str = Form(
        ...,
        min_length=1,
        max_length=20,
        example="Arturo",
    ),
    last_name: str = Form(
        ...,
        min_length=1,
        max_length=20,
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20,
        max_length=300,
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None),
):
    return user_agent

# Files


@app.post(
    path="/post-image",
    tags=["Users"]
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "filesname": image.filename,
        "Size(kb)": round(len(image.file.read()) / 1024, 2),
        "format": image.content_type
    }
