FROM python:3
ADD project_2.py /
RUN pip install opencv-python
RUN pip install numpy
RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y
CMD [ "python", "./project_2.py"]