#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os
import uuid
import pickle

import pandas as pd

import mlflow

from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline


# In[8]:


year = 2023
month = 2
taxi_type = 'green'

input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
output_file = f'output/{taxi_type}_{year:04d}-{month:02d}.parquet'

RUN_ID = '0b2rf6a1ef3c4e6280d5ajfdb94c68ul'


# In[9]:


def generate_uuids(n):
    ride_ids = []
    for i in range(n):
        ride_ids.append(str(uuid.uuid4()))
    return ride_ids

def read_dataframe(filename: str):
    df = pd.read_parquet(filename)

    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]
    
    df['ride_id'] = generate_uuids(len(df))

    return df


def prepare_dictionaries(df: pd.DataFrame):
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']

    categorical = ['PU_DO']
    numerical = ['trip_distance']
    dicts = df[categorical + numerical].to_dict(orient='records')
    return dicts


# In[10]:


def load_model(run_id):
    logged_model = f's3://yahya-mlops/airflow/1/{RUN_ID}/artifacts/model'
    model = mlflow.pyfunc.load_model(logged_model)
    return model


def apply_model(input_file, run_id, output_file):

    df = read_dataframe(input_file)
    dicts = prepare_dictionaries(df)

    
    model = load_model(run_id)
    y_pred = model.predict(dicts)

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['lpep_pickup_datetime'] = df['lpep_pickup_datetime']
    df_result['PULocationID'] = df['PULocationID']
    df_result['DOLocationID'] = df['DOLocationID']
    df_result['actual_duration'] = df['duration']
    df_result['predicted_duration'] = y_pred
    df_result['diff'] = df_result['actual_duration'] - df_result['predicted_duration']
    df_result['model_version'] = run_id
    
    df_result.to_parquet(output_file, index=False)


# In[11]:


apply_model(input_file=input_file, run_id=RUN_ID, output_file=output_file)


# In[ ]:




