# Gwinstek api client

## Conclusion

Implemented a rest api for working with DC power supplies of the GPP-1326/P 2323/GPP-3323/GPP-4323 series

This guide provides instructions on how to set up this project.

### Architecture

```
project
│   run.py                          # main file 
│   .flake8                         # linter
│   .gitignore                      # gitignore file    
|   poetry.lock                     # utomatically generated file that locks the dependencies 
|   poetry.toml                     # main configuration file for Poetry.
|   README.md                       # description file
|
└───gwinstek
│   │   __init__.py                 # batch file
│   │   gwinstek.py                 # consist a class driver
|
└───api
│   │   __init__.py                 # batch file
│   │   app.py                      # a file with the main functionality of the application
|
└───tests
    |   __init__.py                 # package file
    │   test_api.py                 # set of tests that check the correctness of commands issued via tcp-ip
    │   tests_correct_data.py       # set of tests that verify the correctness of processing data received from the device
    |   test_correct_methods.py     # set of tests that verify that when accessing the url, the desired method of the desired class will be called
```

### Quick start

* Python > 3.8;
* Poetry 1.5.1.

### Installation

1. Clone this repo 

```bash
git clone https://github.com/rpopov94/gwinstek-api-client.git
```

2. Change to the project directory:
```bash
cd  gwinstek-api-client
```

3. Install poetry
```bash
pip -U install poetry
```

4. Install dependencies
```bash
poetry install
```

5. Activate the virtual environment created by Poetry:
```bash
poetry shell
```

6. Run project

```bash
uvicorn run:api --host 0.0.0.0 --port 8000
```
Open browser with address http://0.0.0.0:8000/docs

Go to page http://0.0.0.0:8000/docs to get the documentation in swagger

### Description API

Here are the descriptions of the REST API endpoints:

`GET /`

**Description**: Home page.

**Response**: JSON object with a success message with greeting.

`POST /set_current:`

**Description**: Sets the current value for a specific channel.

**Request body**: JSON object containing the channel number and current value.

**Response**: JSON object with a success message and the channel and current values.

`POST /set_voltage:`

**Description**: Sets the voltage value for a specific channel.

**Request body**: JSON object containing the channel number and voltage value.

**Response**: JSON object with a success message and the channel and voltage values.

`POST /enable_channel/{channel}`:

**Description**: Enables a specific channel.

**Path parameter**: Channel number.

**Response**: JSON object with a success message and the channel number.

`POST /disable_channel/{channel}`:

**Description**: Disables a specific channel.

**Path parameter**: Channel number.

**Response**: JSON object with a success message and the channel number.

`GET /get_telemetry:`

**Description**: Retrieves telemetry data for all channels.

**Response**: JSON object with a success message and an array of telemetry values for each channel.

**Note**: In case of any exceptions or errors during the execution of these endpoints, the response will contain a failure message and relevant data as specified in the respective exception handling blocks.

### Run tests

```bash
pytest
```

### References

* [Gwinsteck DC power supplies](https://www.gwinstek.com/en-global/products/downloadSeriesDownNew/14242/1737)
* [Fastapi docs](https://fastapi.tiangolo.com/)
* [Poetry documentation](https://python-poetry.org/docs/)
* [FastAPI with Async SQLAlchemy, SQLModel, and Alembic](https://testdriven.io/blog/fastapi-sqlmodel/)
* [Developing and Testing an Asynchronous API with FastAPI and Pytest](https://testdriven.io/blog/fastapi-crud/)

### License 
MIT