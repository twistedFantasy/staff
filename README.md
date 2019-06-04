# staffy

The Goal of this app is to provide simple staff management(ssm) application to manage employees basic information, skills and absences in a clear and easy way for both employees and staff folks.
Backend will be supported by the power of Python and Django/Django Rest Framework together with additional 3-rd party packages while frontend will feel the power and love of Vue.js.
And of course docker one love!

# Versions
```
Python: 3.7.3
Django: 2.2.1
Django Rest Framework: 3.9.4
PostgreSQL: 11.3
Docker: 18.09.0
docker-compose: 1.23.1
```

# Docker & Docker-Compose install
``` 
https://docs.docker.com/install/linux/docker-ce/fedora/
https://github.com/docker/compose/releases
```

# Use vagrant if you want
```
vagrant up
vagrant ssh
```

# How to run it locally
```
docker-compose -f docker-compose-local.yml up -d
```

# Useful information
```
1) How to check logs
docker-compose -f docker-compose-local.yml logs -f ssm

or just use portainer if terminal scares you

2) How to run tests?
docker-compose -f docker-compose-local.yml exec ssm pytest
docker-compose -f docker-compose-local.yml exec ssm pytest ssm/users/tests/test_views.py
docker-compose -f docker-compose-local.yml exec ssm pytest ssm/users/tests/test_views.py::SSMTokenObtainTestCase
docker-compose -f docker-compose-local.yml exec ssm pytest ssm/users/tests/test_views.py::SSMTokenObtainTestCase::test_token_obtain__staff_user_correct_credentials

3) Check tests coverage
coverage report will be automatically provided in html format after pytest executing by ssm/htmlcov location

4) How to install new package in Pipfile & Pipfile.lock
docker-compose -f docker-compose-local.yml exec ssm pipenv install django==2.2.1
```
