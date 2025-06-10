import pandas as pd

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression

import mlflow
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient

EXPERIMENT_NAME = "HW3"

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment(EXPERIMENT_NAME)

df= pd.read_parquet("yellow_tripdata_2023-03.parquet")
print(df.shape)

def read_dataframe(filename):
    df = pd.read_parquet(filename)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    
    return df

df = read_dataframe("yellow_tripdata_2023-03.parquet")
print(df.shape)

with mlflow.start_run():
    categorical = ['PULocationID', 'DOLocationID']
    train_dicts = df[categorical].to_dict(orient='records')
    dv = DictVectorizer(sparse=True)
    X_train = dv.fit_transform(train_dicts)
    y_train = df['duration'].values
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    model_artifact_path = "hw3_model"
    mlflow.sklearn.log_model(
        sk_model=lr,
        artifact_path=model_artifact_path,
        registered_model_name="HW3Model"
    )
    
print("Intercept:", lr.intercept_)