# Wallet app

A REST API server for managing transactions and wallets.

## Technologies

This project is built using:

- **Python 3.11+**
- **Django Rest Framework (DRF)**
- **MySQL**
- **Docker & Docker Compose**
- **Black** (code formatting)
- **Pylint** (code linting)
- **isort** (for sorting imports)
- **pytest** (for testing)
- **mommy_recipe** (for test data generation)
- **Pre-commit hooks** (for automated code checks before committing)

## Setup and Run Instructions

### Requirements

- [Docker](https://www.docker.com/get-started) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

### Environment Configuration

1. Create a `.env` file in the project root directory and configure your database settings. Here is an example structure for the `.env` file:

    ```env
      MYSQL_ROOT_PASSWORD=supersecretpassword
      MYSQL_DATABASE=wallet
      MYSQL_USER=someuser
      MYSQL_PASSWORD=userpassword
      MYSQL_HOST=mysql
      MYSQL_PORT=3306
      
      TEST_MYSQL_DATABASE=test_wallet
    ```

2. Adjust any other necessary environment variables as needed for the application.

### Running the Project

1. Clone the repository:

    ```bash
    git clone https://github.com/iambrkkdn/wallet_app.git
    ```

2. Navigate to the project directory:

    ```bash
    cd wallet_app
    ```

3. Build and run the Docker containers using Docker Compose:

    ```bash
    docker-compose up --build
    ```

4. To stop the containers, you can use:

    ```bash
    docker-compose down
    ```

### API Documentation

- **Swagger UI** is available at: [http://localhost:8000/api/v1/swagger/](http://localhost:8000/api/v1/swagger/)
- **ReDoc** is available at: [http://localhost:8000/api/v1/docs/](http://localhost:8000/api/v1/docs/)

### Running Tests

We use `pytest` for testing, along with `mommy_recipe` for generating test data.

To run the tests, use:

```bash
docker exec -it web pytest .
```


### Code Formatting and Linting

This project uses black, isort, and pylint to ensure code quality.

To format the code, run:
```
black -S -l 110 .
isort .
```

For linting, use:
```
pylint .
```

### Pre-commit Hooks

The project also uses pre-commit hooks to automatically format and lint code before each commit. To install the pre-commit hooks, run:

```
pre-commit install
```