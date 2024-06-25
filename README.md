# Cryptocurrency Exchange Analytics Pipeline

## Table of Contents

1. [Overview](#overview)
   - [Data Visualization](#data-visualization)
   - [Data Architecture](#data-architecture)
2. [Prerequisites](#prerequisites)
3. [How to Run This Project](#how-to-run-this-project)
4. [Lessons Learned](#lessons-learned)
5. [Contact](#contact)

## Overview
This project implements an automated data pipeline for analyzing cryptocurrency exchange metrics. It extracts data from various sources, transforms it, and loads it into a database for visualization and analysis. The end product is a dashboard that provides a near real-time insights into exchange performance, trading volumes, and market trends.

### Data Visualization

### Data Architecture

This project uses a containerized architecture with Docker to ensure consistency across environments. Python is used for the ETL processes, with separate extraction, transformation, and loading modules. Data is stored in the Motherduck data warehouse, and logging is implemented for monitoring and debugging.

## Prerequisites

Docker and Docker Compose
Python 3.10 
DuckDB/Motherduck
Make (for using the Makefile)
Github

## How to Run This Project
Follow these step-by-step instructions to get the project up and running:
Clone the repository and navigate to the project directory.

bash 
   ```
git clone https://github.com/yourusername/crypto-metrics-dashboard.git
cd crypto-metrics-dashboard
```
Build and start the Docker containers:
bash ```
make docker
```

Run the data pipeline:
Copypython scripts/data_pipeline.py

To run tests:
Copypytest test/unit
pytest test/integration

To stop and remove the containers:
Copydocker-compose down


Project Structure

containers/: Contains Dockerfile and requirements for containerization.
logs/: Logging configuration and log files.
media/: Images for documentation.
scripts/: Main Python scripts including the data pipeline and ETL processes.
test/: Unit and integration tests.
Makefile: Contains commands for common operations.
docker-compose.yml: Defines and configures Docker services.

Lessons Learned
During this project, I gained valuable experience in:

Implementing a modular ETL pipeline
Containerizing a data engineering project with Docker
Setting up logging for better monitoring and debugging
Writing unit and integration tests for data pipelines

In future iterations, I would consider:

Implementing a more robust error handling system
Exploring cloud-based solutions for improved scalability
Incorporating real-time data streaming for more up-to-date analytics

Contact
For any questions or feedback, please reach out to me on LinkedIn or Twitter.
Would you like me to explain or elaborate on any part of this README?
