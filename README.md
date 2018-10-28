[![Build Status](https://travis-ci.org/Ruiru11/store-api-v2.svg?branch=develop)](https://travis-ci.org/Ruiru11/store-api-v2)     [![Coverage Status](https://coveralls.io/repos/github/Ruiru11/food-api/badge.svg?branch=develop)](https://coveralls.io/github/Ruiru11/food-api?branch=develop)
# STORE-API-V2
An api for the store application using postgresql



## Clonning the repo

OS X, Linux & Windows::

```sh
https://github.com/Ruiru11/store-api-v2.git
```



## Installing dependecies 



```sh
pip install -r requirements.txt
```

## Release History

* v1.0
    * CHANGE: integrate a database
    * Implement authentication 



# Endpoints: 
## user-signup(POST) :
- route: https://njeri.herokuapp.com/api/v2/signup
. payload
 ```{ "password":"adminpass","email":"admin@mail.com"}```
 ## user-signin(POST):
- route:https://njeri.herokuapp.com/api/v2/signin
. payload
 ```{ "email":"admin@mail.com","password":"adminpass"}```
 ## creating an product(POST):
- route:https://njeri.herokuapp.com/api/v2/products
. payload
 ```{ "name":"paint","price":"500","description":"oil-paint","category":"Household"}```

 ## getting all products(GET):
- route:https://njeri.herokuapp.com/api/v2/products
 ## getting a specific product using its id(GET):
- route:https://njeri.herokuapp.com/api/v2/products/id
 ## deleting a product(use its specific id)(DELETE):
- route:https://njeri.herokuapp.com/api/v2/product/id
 ## updating a product(use its specific id)(PUT):
- route:https://njeri.herokuapp.com/api/v2/product/id
## create a sale order(POST)
- route: https://njeri.herokuapp.com/api/v2/sales
. payload
 ```{cost:"500","description":"cement,oii-paint"}```
## get all sales(GET): 
- route: https://njeri.herokuapp.com/api/v2/sales
## get a specific sale(GET)
- route: https://njeri.herokuapp.com/api/v2/sales/id
## get a users sales records:
- route: https://njeri.herokuapp.com/api/v2/user-sales/id

* use the given endpoints, data should be from postman  



# Running the api
- on your terminal:
 
 1. git clone https://github.com/Ruiru11/store-api-v2.git
 2. cd into store-api-v2
 3. activate virtualenv
 4. pip install -r requirements.txt
 5. run python settings.py init_db to create tables
 6. run python settings.py create_admin to create admin  
 4. run python run.py to start the server
 5. make sure to have a postgress database 


