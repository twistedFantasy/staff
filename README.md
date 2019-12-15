# staffy![](staffy.gif)

The Goal of this app is to provide simple staff management(ssm) application to manage employees basic information, skills and absences in a clear and easy way for both employees and staff folks.
Backend will be supported by the power of Python and Django/Django Rest Framework together with additional 3-rd party packages while frontend will feel the power and love of Vue.js.
And of course docker one love!

# Amazon AWS + github actions = ❤️
This application use different Amazon AWS services such as IAM, VPC, Security Groups, RDS, ECS and github actions for
CI/CD. [Amazon AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/home.html) is used for infrastructure as a code pattern.
You can easily deploy it by your own, just create Amazon AWS account, execute cdk deploy command to create AWS infrastructe
and configure github secrets(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) for CI/CD

# Versions
```
Python: 3.8.0
Django: 2.2.7
Django Rest Framework: 3.9.4
PostgreSQL: 12.0
Docker: 19.03.5
docker-compose: 1.24.1
...
```

# Local development
Installation & Configuration:
* [virtualbox](./readme/VIRTUALBOX.md)
* [vagrant](./readme/VAGRANT.md)
* [docker](./readme/DOCKER.md)
* [development](./readme/DEVELOPMENT.md)

# Standards
* pep8: max-line-length=119
* [passwords](./readme/PASSWORDS.md)
