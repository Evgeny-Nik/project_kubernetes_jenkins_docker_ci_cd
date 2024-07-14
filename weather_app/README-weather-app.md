# Flask Weather App

This is a Python Flask application that utilizes the Visual Crossing API to fetch and display weather data for a specified location. \
The app handles user requests, retrieves weather data, and displays it on a web page.


## Table of Contents

- [Setup](#setup)
- [Usage](#usage)
- [Docker](#docker)
- [Tests](#tests)
- [Daytime and Nighttime Settings](#daytime-and-nighttime-settings)
- [Version](#version)

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/Evgeny-Nik/project_kubernetes_jenkins_docker_ci_cd
   cd weather_app
   ```

2. Create a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Set the `API_KEY` environment variable to your Visual Crossing API key:
   ```sh
   export API_KEY=your_api_key
   ```

2. Run the Flask app:
   ```sh
   python app.py
   ```

3. Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Docker

To run the app using Docker:

1. Build the Docker image:
   ```sh
   docker build -t weather-app .
   ```

2. Run the Docker container:
   ```sh
   docker run -e API_KEY=your_api_key -p 8000:8000 weather-app
   ```

3. Open your web browser and navigate to `http://localhost:8000/`.

## Tests

To run the unit tests (Docker):

1. Ensure the Flask app is running on `http://localhost:8000`.

2. Run the tests using the `unittest` module:
   ```sh
   docker exec -it <container_name> python -m unittest tests/website_connectivity_unittest.py
   ```

- This test script checks the connectivity to the Flask app's homepage and verifies the status code, modify it to add your own tests.

## Daytime and Nighttime Settings

The app considers the following times for daytime and nighttime:

-  Daytime: 07:00
-  Nighttime: 19:00

These times can be adjusted in the weather_funcs.py file if needed.

## Version

Current version: 1.1.0 (see `version.txt`)

## To Do List

- [ ] Add HTTPS support
- [ ] Set up history, logging and monitoring functions (MongoDB, Elastik Stack, Prometheu/Loki + Grafana)

