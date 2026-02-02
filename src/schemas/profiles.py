from datetime import date

from fastapi import UploadFile, Form, File, HTTPException
from pydantic import BaseModel, field_validator, HttpUrl, Field

from database.models.accounts import GenderEnum
from validation import (
    validate_name,
    validate_image,
    validate_gender,
    validate_birth_date
)

# Write your code here


class ProfileRequestSchema(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    gender: str = Field(...)
    date_of_birth: date = Field(...)
    info: str = Field(...)

    @field_validator("first_name", "last_name")
    def name_must_contain_only_english_letters(cls, value: str):
        validate_name(value)
        return value

    @field_validator("gender")
    def gender_must_be_valid_option(cls, value: str):
        validate_gender(value)
        return value

    @field_validator("date_of_birth")
    def date_must_be_valid_and_adult(cls, value: date):
        validate_birth_date(value)
        return value

    @field_validator("info")
    def info_must_not_be_empty(cls, value):
        if not value or not value.strip():
            raise ValueError("Info field cannot be empty or contain only spaces.")
        return value


class ProfileResponseSchema(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    info: str
    avatar: str

    model_config = {
        "from_attributes": True
    }
