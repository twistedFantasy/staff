# staffy

The Goal of this app is to provide simple staff management application to manage employees basic information, skills and absences in a clear and easy way for both employees and staff folks.
Backend will be supported by the power of Python and Django/Django Rest Framework together with additional 3-rd party packages while frontend will feel the power and love of Vue.js.
And of course docker one love!

# Versions
```
Python: 3.6.8
Django: 2.1.5
Django Rest Framework: 3.9.0
PostgreSQL: 11.1
Docker: 18.09.0
docker-compose: 1.23.1
```

# Docker & Docker-Compose install
``` 
https://docs.docker.com/install/linux/docker-ce/fedora/
https://github.com/docker/compose/releases
```

# How to run it locally
```
cd dockerX
docker-compose -f docker-compose-local.yml -p staff up -d
```
