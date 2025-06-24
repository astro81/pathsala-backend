```toml
name = 'logout'
method = 'POST'
url = 'http://localhost:8000/api/auth/logout/'
sortWeight = 3000000
id = '065f1ddf-9a61-4abb-87d6-c04f55134250'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNzQyNDEyLCJpYXQiOjE3NTA3NDIxMTIsImp0aSI6IjlmNTlkMTNjZjhiMzQ0NTZiNTFmZGI5NzU5MGU0YjA2IiwidXNlcl9pZCI6IjUzNTY1NjVkLTc1OGYtNGQ0My1hODIwLTMxODNhM2JlZGRjMyJ9.T6fY0-v2vvBHh-qyzvEE-GnKfVHRNDyc3g4jSJrtIfU'

[body]
type = 'JSON'
raw = '''
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MDgyODUxMiwiaWF0IjoxNzUwNzQyMTEyLCJqdGkiOiI0NWYzYmM1MTdlYmQ0Zjk3YTI1NGU1ZDhmNmNiOWY1YSIsInVzZXJfaWQiOiI1MzU2NTY1ZC03NThmLTRkNDMtYTgyMC0zMTgzYTNiZWRkYzMifQ.1Ry3HtfE5R3tv9Hj4Y-OWGiMaDvf2jizhRCI4bOtaUk"
  }'''
```
