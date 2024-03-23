
# Equity Store

## Overview

This project is a stock information management system developed in Python. It uses dependency injection for managing dependencies between different components of the system. The project is designed to load stock information from different exchanges and provide an interface to query this information.

## Modules

### Dependency Injection


Dependency Injection (DI) is a fundamental design pattern in software engineering that promotes loose coupling between components, making systems easier to extend and maintain. In our Python Flask microservice, we leverage DI to dynamically manage our service dependencies, enhancing the application's modularity and flexibility. This section explains how to configure DI using a `factory.json` file and how the Python binder is utilized to wire everything together seamlessly.

#### DI Configuration from `factory.json`

Our application relies on a configuration file named `factory.json` to define the bindings for various services within the microservice. This JSON file specifies the relationships between interfaces (or service contracts) and their concrete implementations, along with their lifecycle scopes. Here's a brief overview of each configuration element:

- **Service**: Represents the interface or abstract class that a component in the application depends on. It defines the contract that the implementation class must adhere to.
- **Implementation**: The concrete class that provides the actual functionality behind the service interface. It's this implementation that will be injected where the service interface is required.
- **Scope**: Determines the lifecycle of the service instance. We support different scopes for managing instance creation and reuse:
  - `singleton`: A single instance is created and shared across the application. This instance is reused in all places where this service is injected, ensuring a consistent state throughout the application lifecycle.
  - `request`: A new instance is created for each request. This is useful for ensuring that data does not leak between requests and that services remain stateless with respect to client interactions.

#### Python Binder: Wiring Services Together

The `DependencyInjectionModules` class, which extends from a base `Module` class provided by our DI framework, plays a crucial role in reading the `factory.json` configuration and setting up the DI container. This class uses the Python binder to wire up the dependencies as defined in the JSON file. Here's how it works:

#### Conclusion

By leveraging a JSON-based configuration and the Python binder for dependency injection, our Flask microservice achieves a high degree of modularity and flexibility. This setup allows developers to easily modify service implementations and their lifecycles without changing the application's codebase, streamlining development and maintenance processes. Remember, while powerful, using `eval()` requires caution to avoid security vulnerabilities, so ensure your configuration data is secure and trusted.


### ConfigProvider

The `ConfigProvider` is responsible for providing configuration details to other components of the system. It reads the configuration from a JSON file named `config.json`.
```json
{
  "port": 8080,
  "log_path": "/var/log/stock_info.log",
  "preload_exchanges": "NASDAQ,NYSE",
  "data_source": "database",
  "exchange_query": "SELECT * FROM stocks WHERE exchange = ?",
  "data_sources": {
    "database": {
      "host": "localhost",
      "port": 3306,
      "user": "root",
      "password": "password",
      "database": "stocks"
    }
  }
}
```

### StockRepository

`StockRepository` is an abstract base class that defines the interface for all stock repositories. It has two concrete implementations: `StockRepositoryDisk` and `StockRepositoryDB`.

- `StockRepositoryDisk`: This implementation reads stock information from JSON files stored on disk. The file name is expected to be in the format `{exchange}-stocks.json`.

- `StockRepositoryDB`: This implementation reads stock information from a database. The connection details and query are provided by the `ConfigProvider`.

Both implementations cache the loaded stock information for faster access.

The factory.json file contains the configuration for the StockRepositoryDB and StockRepositoryDisk classes. 
The factory.json file is used to define which instance of the StockRepository class to use. 
```json
{
  "service": "StockRepository",
  "implementation": "StockRepositoryDisk",
  "scope": "singleton"
}

```


### EquityService

`EquityService` is the main service class that uses `StockRepository` to load stock information from different exchanges in parallel using `ThreadPoolExecutor`. It provides methods to query stock information by exchange or by stock code.

## Usage

To use this system, you need to create an instance of `EquityService` and call its `load_exchanges` method to load stock information. After that, you can use `get_equity` and `get_exchange` methods to query stock information.

```python
equity_service = EquityService(injector)
equity_service.load_exchanges()
stock_info = equity_service.get_equity('AAPL')
exchange_info = equity_service.get_exchange('NASDAQ')
```

## Dependencies

- Python
- Flask==3.0.2
- Flask-Cors==3.0.10
- Flask-HTTPAuth==4.8.0
- Flask-Injector==0.15.0
- flask-restx==1.3.0
- flasgger==0.9.7.1
- injector==0.21.0: A lightweight dependency injection framework for Python.

## Configuration

The system is configured through a JSON file named `config.json`. It contains the following settings:

- `port`: The port number for the application.
- `log_path`: The path where log files are stored.
- `preload_exchanges`: A comma-separated list of exchanges to preload.
- `data_source`: The data source to use for loading stock information.
- `exchange_query`: The SQL query to use for loading stock information from the database.
- `data_sources`: A dictionary of data sources. Each data source is a dictionary containing connection details for a database.

