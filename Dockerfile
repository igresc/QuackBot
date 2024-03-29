# FROM alpine:latest
# ENV TZ=Europe/Madrid
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# RUN apk update \
#    && apk add --no-cache python3 py-pip ffmpeg gcc musl-dev python3-dev py3-pynacl \
#    && pip3 install --upgrade pip
FROM igresc/python-ffmpeg:latest
WORKDIR /app
ENV DEBUG=True
COPY req.txt /app/
RUN pip install -r req.txt
COPY data/ /app/data
COPY src/ /app/
CMD ["python3","-u","main.py"]
