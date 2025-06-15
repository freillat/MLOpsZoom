For the environment question:
pipenv install scikit-learn==1.5.0 flask pandas  --python=3.9.12

To build the docker image using the Dockerfile:
docker build -t ride-duration-prediction-service:v1 .

To access the model within docker once the container is running:
docker run -it --rm -p 9696:9696 ride-duration-prediction-service:v1 /bin/bash
then:
python starter.py -y 2023 -m 5