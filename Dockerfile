FROM ubuntu:latest
ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update -y
RUN apt-get install -y python3-pip ffmpeg
WORKDIR /app
ENV DEBUG=True
#VOLUME /data
COPY req.txt /app/
RUN pip install -r req.txt
COPY data/ /app/data
COPY src/ /app/
ENTRYPOINT ["python3"]
CMD ["main.py"]