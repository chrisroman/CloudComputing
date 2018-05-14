FROM mysql:5.7.15

# TODO: Whenever you want to build, you need to set this manually
ENV MYSQL_DATABASE=$RESERVATIONS_DB_NAME \
    MYSQL_ROOT_PASSWORD=$RESERVATIONS_DB_PASSWORD

ADD Dockerfiles/mysql_server/schema.sql /docker-entrypoint-initdb.d

EXPOSE 3306

