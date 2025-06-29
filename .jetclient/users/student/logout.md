```toml
name = 'logout'
description = 'insert access token in the header and refresh token in body to logout'
method = 'POST'
url = '{{url}}/api/auth/logout-all/'
sortWeight = 3000000
id = '2995442e-5286-43c7-b431-fd322ad49b72'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMjU3MzY3LCJpYXQiOjE3NTExNzA5NjcsImp0aSI6IjA4MGRkMmI1OWM1YjQ0NjY4YjhjZTdhMDU0NDQ0YTlkIiwidXNlcl9pZCI6ImY0ZDQ2YzkwLTc0ODAtNGQzOS04NTQ0LTdkNjllOGY5OTIwZSJ9.N4_T8qnHKQQxCvEN2o2h1rHPG1kLVUzTyNpBMmkZxHU'

[body]
type = 'JSON'
raw = '''
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MTUxNjU2NywiaWF0IjoxNzUxMTcwOTY3LCJqdGkiOiI1NDkxOTUwOTdkMzc0OGIyYjhlMDZlNmExNWY5ZmY1NyIsInVzZXJfaWQiOiJmNGQ0NmM5MC03NDgwLTRkMzktODU0NC03ZDY5ZThmOTkyMGUifQ.Q9CrSwpV8LU5oiqe9c1PxpCH2v5s07Z_peZ3De3UfOc"
}'''
```
