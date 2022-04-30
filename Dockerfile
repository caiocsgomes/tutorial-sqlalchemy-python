FROM postgres:9.6

VOLUME /var/lib/postgresql/data

COPY ./init-user-db.sh /docker-entrypoint-initdb.d/

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB postgres

EXPOSE 5432