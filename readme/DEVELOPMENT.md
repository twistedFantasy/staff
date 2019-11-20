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
