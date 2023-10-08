# Cyber Security Base 2023 – Project I

This repository contains a vulnerable web application for the first project of the [Cyber Security Base 2023](https://cybersecuritybase.mooc.fi/module-3.1) course.

## Disclaimer

This project intentionally contains security vulnerabilities. As such, the code within this repository is for demonstration purposes only and should not be run on public networks or widely distributed.

## Features

The project is a basic book review app developed using Django. The following features are included:

- Users can create an account and log in
- Users can read book reviews written by other users
- Users can write and edit book reviews

## Security Flaws

The app presents multiple security vulnerabilities, aligning with the [OWASP Top Ten](https://owasp.org/www-project-top-ten/) list of prevalent security risks. A detailed examination of these vulnerabilities is provided [here](./essay.md).

## Installation

To get started with the project, follow these steps:

1. Clone the repository

    ```bash
    git clone git@github.com:valtterikantanen/csb-project.git
    cd csb-project
    ```

2. Create a virtual environment and activate it

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    You can deactivate the virtual environment at any time by running `deactivate`.

3. Install the dependencies

    ```bash
    pip install -r requirements.txt
    ```

4. Set up a local database and optionally populate it with [sample data](/src/pages/fixtures/sample.json)

    ```bash
    python3 manage.py migrate
    python3 manage.py loaddata sample
    ```

5. Start the development server

    ```bash
    python3 manage.py runserver
    ```
