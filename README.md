# STORAGE AREA MANAGEMENT APPLICATION

### Description
A small REST API using the Rest API to manage processes in the storage area. 
The API allows you to manage goods, inventory, and orders. 
This application based on the FastApi framework with database support using SQLAlchemy 2.0.

### Endpoints
* Products ((POST /products), (GET /products), (GET /products/{id}), (PUT /products/{id}), (DELETE /products/{id}))
* Orders ((POST /orders), (GET /orders), (GET /orders/{id}), PATCH /orders/{id}/status))

### System requirements:
* programming Language - Python ^3.12
* operating system - OS Independent


### Installation 

* ####  clone project
`git clone https://github.com/AniutaP/storage-area-based-on-fastapi.git`

* #### create environment variables

`cd storage-area-based-on-fastapi`

`touch .env`

`cat > .env`

POSTGRES_DB=storage_area_db

POSTGRES_USER=your_user

POSTGRES_PASSWORD=your_password

POSTGRES_HOST=database

POSTGRES_PORT=5432

`CTRL + D`

* #### start docker command 

`sudo docker-compose up --build`

* #### configuring database tables

`sudo docker-compose exec web alembic upgrade head`


### Database simple backup
`pg_dump -h <host> -U <user> -d <dbname> -f backup.sql`