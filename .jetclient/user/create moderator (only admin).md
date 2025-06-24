```toml
name = 'create moderator (only admin)'
method = 'POST'
url = 'http://localhost:8000/api/auth/create-moderator/'
sortWeight = 7000000
id = 'd4c0ed78-15f8-43f3-9a59-6a219f0dc805'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNzYxNTgxLCJpYXQiOjE3NTA3NjEyODEsImp0aSI6IjgwNTdhYjcxN2I0NjRlNWM4ZDY2YjUxZTJmZDhhMmYxIiwidXNlcl9pZCI6IjY4OGQzOWIzLWI2YzItNDU1MC1iOWMzLWQyZTIyZjM1YzFiNSJ9.XLXCaquNCP8B_XZ9SSI2xreDojRHqPVG81JHWzFIc6w'

[body]
type = 'JSON'
raw = '''
{
  "username": "moderator_User3",
  "email": "moderator_User22@example.com",
  "password": "Adminpassword1@",
  "password2": "Adminpassword1@"
}
'''
```
