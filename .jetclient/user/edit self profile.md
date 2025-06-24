```toml
name = 'edit self profile'
method = 'PATCH'
url = 'http://localhost:8000/api/auth/user/edit/'
sortWeight = 5000000
id = '8c70fd9d-e004-4690-b0ad-8771f62b2591'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNzQxNjU1LCJpYXQiOjE3NTA3NDEzNTUsImp0aSI6ImU3MGU5MzMwMDM3YTRmYWViNTkzN2JhMzcyN2ZjZWViIiwidXNlcl9pZCI6IjUzNTY1NjVkLTc1OGYtNGQ0My1hODIwLTMxODNhM2JlZGRjMyJ9.KrMBhpnKvKFkqF9b96Ls_xBCi4BYYuBCiwrlgYw5cgM'

[body]
type = 'JSON'
raw = '''
{
  "username": "pathsalla",
  "email": "pathsala@gmail.com",
  "password": "securePass@123",
  "password2": "securePass@123",
  "first_name": "path",
  "last_name": "sala",
  "address": "123 Street, City",
  "phone_no": "+997-981234567"
}
'''
```
