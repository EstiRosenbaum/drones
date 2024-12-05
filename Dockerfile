FROM python:3.12.2

WORKDIR /app

COPY ./ /app

EXPOSE 8000

RUN  pip install .

CMD [ "flet" , "run" , "-d" , "--web" , "--port" , "8000" , "src/main.py" ]
