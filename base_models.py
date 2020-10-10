from pydantic import BaseModel

class Features(BaseModel):
    user_id: int
    age: int
    workclass: str
    fnlwgt: int
    education: str
    education_num: int
    marital_status: str
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: int
    capital_loss: int
    hours_per_week: int
    native_country: str

    def __getitem__(cls, feature):        
        return cls.__dict__[feature]