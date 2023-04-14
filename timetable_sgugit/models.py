from pydantic import BaseModel


class LessonAddRequest(BaseModel):

    hour_id        : int
    lesson_type_id : int
    audience       : int
    group_id       : int
    teacher_id     : int
    lesson_name_id : int
    date           : str


class LessonParseResult(BaseModel):

    hour        : str
    lesson_type : str
    audience    : str
    group       : str
    teacher     : str
    lesson_name : str
    date        : str


class GroupCreateRequest(BaseModel):

    sgugit_id      : int
    name           : str
    course         : int
    institute      : int
    education_form : int


class AudienceCreateRequest(BaseModel):

    name     : str
    building : int


class LessonInfoModel(BaseModel):

    id          : int
    hour        : int
    lesson_type : int
    audience    : str
    group       : str
    teacher     : str
    lesson_name : str
    date        : str
