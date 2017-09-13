FROM jupyter/minimal-notebook

MAINTAINER Eric Sherman <ericandrewsherman@gmail.com>

COPY . /app

WORKDIR /app

RUN pip install -r ./app/requirements.txt

EXPOSE 8888:8888

ENTRYPOINT ["jupyter", "notebook"]

