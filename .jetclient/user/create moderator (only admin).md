```toml
name = 'create moderator (only admin)'
method = 'POST'
url = 'http://localhost:8000/api/auth/create-moderator/'
sortWeight = 7000000
id = 'd4c0ed78-15f8-43f3-9a59-6a219f0dc805'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwODE5Njg3LCJpYXQiOjE3NTA4MTkzODcsImp0aSI6ImZiNTZhN2UzZTM2MjQyZDk4M2MyMjY1YjY1MzdiZmFjIiwidXNlcl9pZCI6IjY4OGQzOWIzLWI2YzItNDU1MC1iOWMzLWQyZTIyZjM1YzFiNSJ9.NywBbf-HA1iq0FVLD_Eks_YPPI-gdIkk37Z4y_l5EnM'

[body]
type = 'JSON'
raw = '''
{
  "username": "moderator_User3",
  "email": "moderator_User33@example.com",
  "password": "Adminpassword1@",
  "password2": "Adminpassword1@"
}
'''
```
