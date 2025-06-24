# Dependencies
### PIP
```shell
pip install uv
```
### Nix-Shell
```shell
nix-shell -p uv python312
```

## Required Libraries
```python
django django-role-permissions djangorestframework pillow djangorestframework-simplejwt drf-yasg
```

# Create Super Admin
```shell
uv run python manage.py createadmin
``` 

## Run Server
```shell
uv run python manage.py runserver
```