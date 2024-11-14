# STORAGE AREA MANAGEMENT APPLICATION

### Description
A small REST API using the Rest API to manage processes in the storage area. 
The API allows you to manage goods, inventory, and orders. 
This application based on the FastApi framework with database support using SQLAlchemy 2.0.

### Endpoints
* Login

`POST /login/token`
* Users 

`GET /users, GET /users/{id}, GET /users/{id}/orders, GET /users/{id}/total`

`POST /users, PUT /users/{id}, DELETE /users/{id}`
* Products 

`GET /products, GET /products/{id}, POST /products, PUT /products/{id}, DELETE /products/{id}`
* Orders 

`GET /orders, GET /orders/{id}, POST /orders, PATCH /orders/{id}/status`

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

ADMIN_EMAIL=admin_email

ADMIN_PASSWORD=admin_password

`CTRL + D`

* #### start docker command 

`sudo docker-compose up --build`

* #### configuring database tables

`sudo docker-compose exec web alembic upgrade head`


### Database simple backup
`pg_dump -h <host> -U <user> -d <dbname> -f backup.sql`