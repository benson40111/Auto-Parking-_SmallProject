FROM vekerdyb/rpi-python3

COPY requirements.txt ./

RUN python3 -m pip install -r requirements.txt

WORKDIR /usr/src/app

CMD ["top", "-b"]
#CMD ["python3", "main.py"]
