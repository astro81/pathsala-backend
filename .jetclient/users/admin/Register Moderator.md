```toml
name = 'Register Moderator'
description = '- Only Admin can create a moderator'
method = 'POST'
url = '{{url}}/api/auth/register/moderator/'
sortWeight = 3000000
id = '93b107b5-afab-4cbd-9e9d-58a68cfe206e'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNzg0NDQxLCJpYXQiOjE3NTE2OTgwNDEsImp0aSI6Ijc2ZTczMGE4MTJkNjQ0YjRiZWY0ZjRjMjZkY2MyZDQ3IiwidXNlcl9pZCI6ImY0OWY4NjhhLTViYmMtNGE3Mi04MjY2LTBhMjA4OGQ0ZDI4MCJ9.oek7kqXLRzsOSeZf1zfk7XU3UDh-_nllohC1RTwVcWg'

[body]
type = 'JSON'
raw = '''
{
  "username": "mod1",
  "email": "mod1@sys.com",
  "password": "Mod@1234",
  "password2": "Mod@1234",
  "first_name": "mod",
  "last_name": "sys"
}'''
```
