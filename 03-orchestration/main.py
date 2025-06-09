import pandas as pd

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression

import mlflow
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient

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

def train(df):
    categorical = ['PULocationID', 'DOLocationID']
    train_dicts = df[categorical].to_dict(orient='records')
    dv = DictVectorizer(sparse=True)
    X_train = dv.fit_transform(train_dicts)
    y_train = df['duration'].values
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    return dv, lr

dv, lr = train(df)
print("hello")
print("Intercept:", lr.intercept_)
# y_pred = lr.predict(X_train)

def run_register_model(data_path: str, top_n: int):

    client = MlflowClient()

    # Retrieve the top_n model runs and log the models
    experiment = client.get_experiment_by_name(HPO_EXPERIMENT_NAME)
    runs = client.search_runs(
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=top_n,
        order_by=["metrics.rmse ASC"]
    )
    for run in runs:
        train_and_log_model(data_path=data_path, params=run.data.params)

    # Select the model with the lowest test RMSE
    experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
    best_run = client.search_runs(
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=top_n,
        order_by=["metrics.test_rmse ASC"]
    )[0]
    run_id = best_run.info.run_id
    model_uri = f"runs:/{run_id}/model"

    # Register the best model
    mlflow.register_model(model_uri, "best model")


# if __name__ == '__main__':
#     run_register_model()