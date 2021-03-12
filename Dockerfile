FROM python:3
WORKDIR /opt/marvel/

RUN pip3 install requests
RUN pip3 install PyYAML
COPY main.py /main.py
COPY .configs.yaml /.configs.yaml

ENTRYPOINT ["python3", "main.py"]