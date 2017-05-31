FROM python:3-onbuild

COPY ./ ./

RUN chmod +x prepare.sh
RUN ./prepare.sh
RUN chmod +x run_celery.sh
RUN chmod +x run_web.sh
