#Dockerfile
FROM apache/airflow:2.9.0

#run everything as airflow user
USER airflow

#so that the dbt cli is available in the PATH
ENV PATH="${PATH}:/home/airflow/.local/bin"

#Install dbt-core and dbt-postgres into this image
RUN pip install --no-cache-dir dbt-core dbt-postgres

