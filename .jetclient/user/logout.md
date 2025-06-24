```toml
name = 'logout'
method = 'POST'
url = 'http://localhost:8000/api/auth/logout/'
sortWeight = 3000000
id = '065f1ddf-9a61-4abb-87d6-c04f55134250'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNzQxNzQyLCJpYXQiOjE3NTA3NDE0NDIsImp0aSI6Ijg5NThmYjQ0OGU0ODQzYzU5ODdhODZkNDk4MGFlNTE0IiwidXNlcl9pZCI6IjUzNTY1NjVkLTc1OGYtNGQ0My1hODIwLTMxODNhM2JlZGRjMyJ9.au1O0CYh6syLL2T1BQGJ9GZVeuUHNN1i301z4notBp4'

[body]
type = 'JSON'
raw = '''
{
  "refresh" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MDgyNzg0MiwiaWF0IjoxNzUwNzQxNDQyLCJqdGkiOiIwYzE4Y2UwMDQzNTk0YjE0OGNlYTM5YzA1YTMzNzM0NSIsInVzZXJfaWQiOiI1MzU2NTY1ZC03NThmLTRkNDMtYTgyMC0zMTgzYTNiZWRkYzMifQ.i9LElEZmuSyrB9qi76rzAdBajkfNhUnAO_aTPuRbfGk"
}'''
```
