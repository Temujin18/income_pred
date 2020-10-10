from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import pandas as pd
import redis
from datetime import timedelta

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

model = load("model/census_model.joblib")

r = redis.Redis()

def encode_input(X_input):
    for category in categorical:
        X_input[category] = le.fit_transform(X_input[category])
    
    X_input = pd.DataFrame(scaler.fit_transform(X_input), index=X_input['user_id'], columns=X_input.columns)

    return X_input.drop('user_id', axis=1)

@app.post("/predict/")
async def predict_income(features: List[Features]):

    result = []
    X_input = pd.DataFrame()
    for feature in features:
        X_input = X_input.append(feature.__values__, ignore_index=True)

    users = X_input['user_id'].astype(int)

    X_input = encode_input(X_input)

    with r.pipeline() as pipe:
        for user in users:
            if r.exists(user):
                result.append({'user_id' : user, 'income' : r.get(user)})
            else:
                pred = model.predict(X_input.loc[user].values.reshape(1,-1))
                pipe.setex(user, timedelta(minutes=10), ''.join(pred))
                result.append({'user_id' : user, 'income' : ''.join(pred)})

        pipe.execute()
    

    return result