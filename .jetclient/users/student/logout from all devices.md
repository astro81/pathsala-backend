```toml
name = 'logout from all devices'
description = 'insert access token in the header and refresh token in body to logout'
method = 'POST'
url = '{{url}}/api/auth/logout/'
sortWeight = 4000000
id = '5c12ce79-44b0-4acd-8291-d40653f71682'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMjAwNzQ5LCJpYXQiOjE3NTExMTQzNDksImp0aSI6ImYzNDY4M2VjNjBjMTQ5ZDViODVmYTU5ZTE2ZDNmZmIzIiwidXNlcl9pZCI6IjkyOTg0NDRjLTZkZTAtNDQ0Yi05MTU4LWRlNDM1YWNlNTRiYSJ9.F-x5OrIj551keTmwigrh3N34MiA5vV7TyctKY7NADKA'

[body]
type = 'JSON'
raw = '''
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MTQ1OTk0OSwiaWF0IjoxNzUxMTE0MzQ5LCJqdGkiOiIxM2U3ZDQyZDMxODA0Y2NmYjA5NDMwY2Y1YTNlMjRjMCIsInVzZXJfaWQiOiI5Mjk4NDQ0Yy02ZGUwLTQ0NGItOTE1OC1kZTQzNWFjZTU0YmEifQ.0n_OrOE2kJZFpK7IW5MEVfKFVzAYeYLsFNJXsCNDh2s"
}'''
```
