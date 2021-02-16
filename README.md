# Rookly

[![Build Status](https://circleci.com/gh/RooklyBR/rookly-engine.svg?style=svg)](https://circleci.com/gh/RooklyBR/rookly-engine)
[![Python Version](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/)


## Environment Variables

You can set environment variables in your OS, write on ```.env``` file or pass via Docker config.

| Variable | Type | Default | Description |
|--|--|--|--|
| SECRET_KEY | ```string```|  ```None``` | A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.
| DEBUG | ```boolean``` | ```False``` | A boolean that turns on/off debug mode.
| BASE_URL | ```string``` | ```http://api.rookly.com.br``` | URL Base Rookly Engine Backend.
| ALLOWED_HOSTS | ```string``` | ```*``` | A list of strings representing the host/domain names that this Django site can serve.
| DEFAULT_DATABASE | ```string``` | ```sqlite:///db.sqlite3``` | Read [dj-database-url](https://github.com/kennethreitz/dj-database-url) to configure the database connection.
| LANGUAGE_CODE | ```string``` | ```en-us``` | A string representing the language code for this installation.This should be in standard [language ID format](https://docs.djangoproject.com/en/2.0/topics/i18n/#term-language-code).
| TIME_ZONE | ```string``` | ```UTC``` | A string representing the time zone for this installation. See the [list of time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
| STATIC_URL | ```string``` | ```/static/``` | URL to use when referring to static files located in ```STATIC_ROOT```.
| EMAIL_HOST | ```string``` | ```None``` | The host to use for sending email. When setted to ```None``` or empty string, the ```EMAIL_BACKEND``` setting is setted to ```django.core.mail.backends.console.EmailBackend```
| EMAIL_PORT | ```int``` | ```25``` | Port to use for the SMTP server defined in ```EMAIL_HOST```.
| DEFAULT_FROM_EMAIL | ```string``` | ```webmaster@localhost``` | Default email address to use for various automated correspondence from the site manager(s).
| SERVER_EMAIL | ```string``` | ```root@localhost``` | The email address that error messages come from, such as those sent to ```ADMINS``` and ```MANAGERS```.
| EMAIL_HOST_USER | ```string``` | ```''``` | Username to use for the SMTP server defined in ```EMAIL_HOST```.
| EMAIL_HOST_PASSWORD | ```string``` | ```''``` | Password to use for the SMTP server defined in ```EMAIL_HOST```.
| EMAIL_USE_SSL | ```boolean``` | ```False``` | Whether to use an implicit TLS (secure) connection when talking to the SMTP server.
| EMAIL_USE_TLS | ```boolean``` | ```False``` | Whether to use a TLS (secure) connection when talking to the SMTP server.

