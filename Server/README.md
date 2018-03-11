# Cloud Computing

## Virtual Environment

Make sure you have [`virtualenv`](https://virtualenv.pypa.io/en/stable/) installed.  
On creating a `virtualenv` called `venv`, run the following:

````bash
pip install git+https://github.com/cuappdev/appdev.py.git#egg=appdev.py
pip install -r requirements.txt
````

## Setting up Database

To be able to run this locally, you will need mongodb installed on your computer. Once that's done, make sure the directory `/data/db/` exists on your machine. Before running the server for this app, run `mongod` to start a MongoDB server on localhost and port 27017.

## Environment Variables

I highly recommend [`autoenv`](https://github.com/kennethreitz/autoenv).
The required environment variables for this API are the following:

````bash
DB_USERNAME
DB_PASSWORD
DB_HOST
DB_NAME
TEST_DB_USERNAME
TEST_DB_PASSWORD
TEST_DB_HOST
TEST_DB_NAME
APP_SETTINGS # e.g. config.DevelopmentConfig
````
If using `autoenv` for local development, create a `.env` file, like the sample below:
````bash
export DB_USERNAME=CHANGEME
export DB_PASSWORD=CHANGEME
export DB_HOST=localhost
export DB_NAME=pcasts_db_dev
export TEST_DB_USERNAME=CHANGEME
export TEST_DB_PASSWORD=CHANGEME
export TEST_DB_HOST=localhost
export TEST_DB_NAME=test_pcasts_db_dev
export APP_SETTINGS=config.DevelopmentConfig
````

In the `/tests` directory, create another `.env` file that changes the `APP_SETTINGS`:
````bash
export APP_SETTINGS=config.TestingConfig
````

## Testing
To run all unit tests, from the `/tests` directory, run:
````
./test.sh
````

To run a single test, from the `/tests` directory, run:
````
./test.sh test_file_name.py
````
