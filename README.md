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

POSTGRES_HOST=your_host

POSTGRES_PORT=5432

`CTRL + D`

* #### start docker command 

`docker-compose up --build`


### Database simple backup
`pg_dump -h <host> -U <user> -d <dbname> -f backup.sql`