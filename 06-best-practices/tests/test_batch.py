#!/usr/bin/env python
# coding: utf-8

import batch
import pandas as pd

from datetime import datetime

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
]

columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
df = pd.DataFrame(data, columns=columns)

data_output = [
    ("-1", "-1", dt(1, 1), dt(1, 10), 9.0),
    ("1", "1", dt(1, 2), dt(1, 10), 8.0)    
]

columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'duration']
df_output = pd.DataFrame(data_output, columns=columns)

def test_prepare_data():
    categorical = ['PULocationID', 'DOLocationID']    
    df_result = batch.prepare_data(df, categorical)    
    assert df_result.equals(df_output)