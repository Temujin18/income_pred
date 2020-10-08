from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
from sklearn.preprocessing import StandardScaler
import pandas as pd

from training import le, scaler, X, categorical

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

app = FastAPI()

model = load("census_model.joblib")

@app.post("/predict/")
async def predict_income(features: List[Features]):

    X_input = pd.DataFrame()
    result = []
    for feature in features:
        X_input = X_input.append(feature.__values__, ignore_index=True)

    users = X_input['user_id']
    X_input = X_input.drop(['user_id'], axis=1)
    
    for category in categorical:
        X_input[category] = le.fit_transform(X_input[category])
    
    X_input = pd.DataFrame(scaler.fit_transform(X_input), columns=X_input.columns)

    preds = model.predict(X_input)
    for user, pred in zip(users, preds):
        result.append({'user_id' : user, 'income' : str(pred)}) 

    return result