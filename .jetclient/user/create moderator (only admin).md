```toml
name = 'create moderator (only admin)'
method = 'POST'
url = 'http://localhost:8000/api/auth/create-moderator/'
sortWeight = 7000000
id = 'd4c0ed78-15f8-43f3-9a59-6a219f0dc805'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNjkwNzk0LCJpYXQiOjE3NTA2OTA0OTQsImp0aSI6ImI3ODRhMTkxOGIwNjQxMGM4NjI3MGVjMDRjZGE5MzdhIiwidXNlcl9pZCI6IjliN2YzMmMyLThlYmQtNGI2NS1hMTA5LWRhYjU4NGNhNThmNiJ9._SgLEjMShKxf8AK_NRgQAavTh-Dm0yWnZKAg468nvpg'

[body]
type = 'JSON'
raw = '''
{
  "username": "moderator_User",
  "email": "moderator_User@example.com",
  "password": "Adminpassword1@",
  "password2": "Adminpassword1@"
}
'''
```
