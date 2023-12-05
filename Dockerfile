FROM python:3.10.13-bullseye

RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python

WORKDIR /workspace
COPY ./requirements.txt .

RUN pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]