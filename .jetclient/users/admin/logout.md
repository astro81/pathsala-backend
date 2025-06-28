```toml
name = 'logout'
description = '- logout the admin'
method = 'POST'
url = '{{url}}/api/auth/logout/'
sortWeight = 2000000
id = 'c04a3fa9-0058-4ea3-8aea-256e19d3f3f4'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMjAyMzQ4LCJpYXQiOjE3NTExMTU5NDgsImp0aSI6IjVlNWQ4MTI4Mzc1NzQ3ODQ4NGE5Nzc5N2U0MWFjYWRiIiwidXNlcl9pZCI6ImI4ZjVlOTZhLTI1ZDgtNDEyMS1hNTRiLTIxNzIyNzVlMTRkZCJ9.Cy2Vqy1TEVVh71Otns60Kmex_2lB9qrVwIHWHDFXMpc'

[body]
type = 'JSON'
raw = '''
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MTQ2MTU0OCwiaWF0IjoxNzUxMTE1OTQ4LCJqdGkiOiI0MGZjOGRiNWE5OTY0Y2FlOWI1NGRjOGI0NzJiMmRkYyIsInVzZXJfaWQiOiJiOGY1ZTk2YS0yNWQ4LTQxMjEtYTU0Yi0yMTcyMjc1ZTE0ZGQifQ.Fta6NXGS1qSKdY_wbLF6ql3e7BqmzPmgd688BnW7Gjo"
}'''
```
