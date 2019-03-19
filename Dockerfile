FROM duckietown/amod:aido2-01

WORKDIR /project

COPY requirements.txt .
RUN pip3.7 install -r requirements.txt

COPY solution.py .
COPY src /project/src

ENV PYTHONPATH=/project/src
CMD python3.7 /project/solution.py


