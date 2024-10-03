###############################################
# Dockerfile to build request_udn_files.py container image
#   docker build -t gvcn/request_udn_files:v0.0.5 . --platform linux/amd64
#   docker push gvcn/request_udn_files:v0.0.5
#   docker run -v $PWD:$PWD gvcn/request_udn_files:v0.0.5 python /home/bin/request_udn_files.py -a $PWD/${api_token_file} -u ${udn_id} -p $PWD
###############################################
FROM python:3.8-slim-buster
# Copy python script
ADD request_udn_files.py .
RUN apt-get -y update && \
    apt-get -y install curl && \
    pip install 'requests==2.27.1' && \
    mkdir /home/bin && \
    cp request_udn_files.py /home/bin
ENV PATH=/home/bin:${PATH}
