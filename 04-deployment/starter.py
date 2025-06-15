import argparse
import pickle
import pandas as pd

parser = argparse.ArgumentParser(description="Process data for a specific year and month.")
parser.add_argument('--year', '-y', type=int, required=True,
                    help='The year (e.g., 2024)')
parser.add_argument('--month', '-m', type=int, required=True,
                    help='The month (1-12)')
args = parser.parse_args()
year = args.year
month = args.month

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet')

dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)

print(y_pred.mean())
print(y_pred.std())

df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
df_result = pd.DataFrame()
df_result['ride_id'] = df['ride_id']
df_result['pref'] = y_pred

output_file=f'{year:04d}-{month:02d}_output.parquet'
df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)