docker build -t ride-duration-prediction-service:v1 .

docker run -it --rm -p 9696:9696 ride-duration-prediction-service:v1 /bin/bash

then:

python starter.py -y 2023 -m 5