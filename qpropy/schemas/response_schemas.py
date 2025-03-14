from pydantic import BaseModel
from typing import Optional, List


class CustomVariables(BaseModel):
    custom1: Optional[str]
    custom2: Optional[str]
    custom3: Optional[str]
    custom4: Optional[str]
    custom5: Optional[str]


class Location(BaseModel):
    country: Optional[str]
    countryCode: str
    latitude: float
    longitude: float
    region: str
    radius: int


class AnswerValue(BaseModel):
    scale: str
    other: str
    dynamicExplodeText: str
    text: str
    result: str
    fileLink: str
    weight: float


class AnswerItem(BaseModel):
    answerID: int
    answerText: str
    value: AnswerValue


class ResponseItem(BaseModel):
    questionID: int
    questionCode: str
    questionDescription: str
    imageUrl: Optional[str]
    questionText: str
    answerValues: List[AnswerItem]


class Response(BaseModel):
    responseID: int
    surveyID: int
    surveyName: str
    ipAddress: str
    timestamp: str
    utctimestamp: str
    language: str
    duplicate: bool
    responseStatus: str
    operatingSystem: str
    customVariables: CustomVariables
    externalReference: str
    osDeviceType: str
    timeTaken: int
    currentInset: str
    utctimestamp: int
    browser: str
    location: Location
    responseSet: List[ResponseItem]
