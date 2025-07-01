```toml
name = 'Register Moderator'
description = '- Only Admin can create a moderator'
method = 'POST'
url = '{{url}}/api/auth/register/moderator/'
sortWeight = 3000000
id = '93b107b5-afab-4cbd-9e9d-58a68cfe206e'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNDI1MTkxLCJpYXQiOjE3NTEzMzg3OTEsImp0aSI6IjMyZDk0MDc5OGY1NjRiMTA5ZDEzZDIyMWQ1MWIxMjIzIiwidXNlcl9pZCI6ImMzZWI5NjE1LTg2ODUtNDI1OC04ZDJmLWQ3MjMzZGI3MTJkNiJ9.gF0DjGDwwS8XNrfelFcMXsID99JEDI7n_rBtb9DVqxw'

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
