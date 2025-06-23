```toml
name = 'logout'
method = 'POST'
url = 'http://localhost:8000/api/auth/logout/'
sortWeight = 3000000
id = '065f1ddf-9a61-4abb-87d6-c04f55134250'

[[headers]]
key = 'Authorization'
value = '"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MDc3Njc1MiwiaWF0IjoxNzUwNjkwMzUyLCJqdGkiOiIxYWJlMTQ1NDU0ZjA0ZGFlOTQzNzZlNzRjYTM5NTljYyIsInVzZXJfaWQiOiJkNTE4MDYwMC1hMzI1LTRkYmYtOTYzOS0zNzU0NmY2ZmZjMjUifQ.8Nc4vi4UXa0TYvu7TTc7RU4BIF0-Uh0C8waoxBJUda0"'

[body]
type = 'JSON'
raw = '''
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MDc3Njc1MiwiaWF0IjoxNzUwNjkwMzUyLCJqdGkiOiIxYWJlMTQ1NDU0ZjA0ZGFlOTQzNzZlNzRjYTM5NTljYyIsInVzZXJfaWQiOiJkNTE4MDYwMC1hMzI1LTRkYmYtOTYzOS0zNzU0NmY2ZmZjMjUifQ.8Nc4vi4UXa0TYvu7TTc7RU4BIF0-Uh0C8waoxBJUda0"
}'''
```
