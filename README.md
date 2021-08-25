### Using Pytest
Set an environment variable for `DJANGO_SETTINGS_MODULE`.

For example:
```shell
export DJANGO_SETTINGS_MODULE=votepredictbackend.settings
```

### Gunicorn Notes
Set the following environment variable to enable auto-reload:
```shell
export RELOAD=--reload
```