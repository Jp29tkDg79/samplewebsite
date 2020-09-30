FROM python:3

# copy package file
COPY  requirements.txt /

# update pip and install packages
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# create work directory
WORKDIR /
RUN mkdir /work
