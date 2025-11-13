# Project Brief: Pokémon Scouting Data Implementation
We are a team of Pokémon trainers utilizing PokeAPI (https://pokeapi.co/) as the primary source
for data related to Pokémon. As part of our scouting efforts, we aim to streamline the process of
retrieving, sanitizing, and formatting Pokémon data to assist our scouts in making informed
decisions.

## 1. Objectives
We need to accomplish the following:

### 1.1 Build an App for Data Intake and Processing
* Retrieve data for the following Pokémon:
  * Pikachu
  * Dhelmise
  * Charizard
  * Parasect
  * Terodactyl
  * Kingler

* Sanitize and format the data: Based on our business logic, retrieve any data points you deem necessary
* Store the data in a SQLite database
* Utilize SQLAlchemy as the ORM
* Use Flask as the core framework of the application

### 1.2. Reusable Process and App
* Design the app to be reusable for future Pokémon scouting tasks with minimal configuration changes.
* Ensure the app handles the end-to-end process of retrieving, sanitizing, formatting, and exporting data for any Pokémon.

### 1.3. Comprehensive Documentation
* Provide detailed documentation for all components of the project.



## 2. Deliverables

### 2.1. Python Flask App
* A functioning Python-based application that retrieves, processes, exports,
and stores the requested Pokémon data in the database. Please provide this
on a public GitHub repository.

### 2.2. Include a document file with:
* Instructions for setting up and running the app.
* An explanation of how to configure the app for other Pokémon.
* Any additional documentation needed.

### 2.3. Swagger
* Swagger implementaded with all documented endpoints

### 2.4. Unit tests with Pytest
* All endpoints, functions, methods must have tests with 100% of coverage
* Implement the coverage tool, to ensure the metrics



## 3. Guidelines
* This project have to implement best practices of development, taking in considerations:

### 3.1. Data structures and Algorithms
* Best practices of DSA
* With less complexity of time and space possible

### 3.2. Security
* Ensuring best practices of security
* Not allowing vulnerable implementations

### 3.3. The Zen of Python
* Remembering all knowledge implemented as filosofy

```
$ python

>>> import this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```
