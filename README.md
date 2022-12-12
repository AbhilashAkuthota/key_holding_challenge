# Key Holding Challenge (Using a simple django rest framework)

pre requisites:
  - docker setup
  - python3 (at least 3.8)

make commands to set up the project:

    - make env-setup
        Creates a virtual environment in the current directory.
    - make setup-docker
        Creates a docker container with postgres (all the data
        is persisted in the volume) and django server.
    - make pre-fill-db
        To fill the db with countries so that it is used in the apis.
    - make django
        To run the django project
    - make run-tests
        To run all the tests defined in the project
    - make pre-commit-mac
        Not required to run the project but it is used to setup
        pre commit hooks which are defined in the .pre-commit-config.yaml.
        This command works only for mac.
---


Note:
---
    The project uses 8000 for the server and 5432 for the postgres.
---

Important Points:
---
- swagger endpoints are available at: http://0.0.0.0:8000/swagger/
- Admin pages are available at: http://0.0.0.0:8000/admin/
- Unit tests and API tests are added in the tests.py for the travel app.
- buildspec.yaml represents the code pipeline to run tests, build the docker image and push it to the respective docker repository as defined in the environment.

To run the project:
---
- Execute the command "make setup-docker" which will start the postgres db and django server.
- Only the requests from 0.0.0.0 are accepted by the server. (It is defined in the config used by the docker)

Missing Features:
---
1. Pushing logs to a proper log aggregator.
2. Adding type hinting to the entire project.

Total Time spent on the project so far: 7-8 hours.
