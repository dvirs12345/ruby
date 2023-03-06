FROM python:3
ADD readLicensePlate.py readLicensePlate.py
ADD server.py server.py
EXPOSE 8888
ENTRYPOINT ["python3", "server.py"]
