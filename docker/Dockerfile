FROM python:3.8-alpine

RUN apk add --no-cache git gcc
RUN apk add --no-cache gcc g++ make libffi-dev python3-dev build-base
RUN apk add --no-cache jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

RUN pip install ipdb
RUN pip install ipython

WORKDIR /app

RUN git clone https://github.com/PGPI-3-7/acme-wedding .
RUN git checkout -b develop origin/develop
RUN pip install -r ./requirements.txt

COPY docker-settings.py ./settings.py

EXPOSE 8000

COPY startdjango.sh .

CMD "./startdjango.sh"