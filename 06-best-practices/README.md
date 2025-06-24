Question 4
docker-compose up -d

export AWS_ACCESS_KEY_ID="test"
export AWS_SECRET_ACCESS_KEY="test"
export AWS_DEFAULT_REGION="us-east-1"

aws s3 mb s3://nyc-duration --endpoint-url=http://localhost:4566
aws s3 ls --endpoint-url=http://localhost:4566

set variables
export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
export S3_ENDPOINT_URL="http://localhost:4566"

Question 5

to get the size of the file after running pytest /tests/integration_test.py
aws s3 ls s3://nyc-duration/in/ --endpoint-url=http://localhost:4566