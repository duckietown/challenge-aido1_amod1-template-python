FROM duckietown/amod:latest

RUN apt-get update
RUN apt-get install -y python-pip

COPY requirements.txt /project/requirements.txt
RUN pip install -r /project/requirements.txt

COPY solution.py /project/solution.py
COPY src /project/src


WORKDIR /project

ENV PYTHONPATH=/project/src
CMD python2 /project/solution.py


