FROM mysql:5.7.15

ENV MYSQL_DATABASE=ParkingFinder \
    MYSQL_ROOT_PASSWORD=INSERT_PASSWORD_HERE

ADD schema.sql /docker-entrypoint-initdb.d

EXPOSE 3306
