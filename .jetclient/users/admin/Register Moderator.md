```toml
name = 'Register Moderator'
description = '- Only Admin can create a moderator'
method = 'POST'
url = '{{url}}/api/auth/register/moderator/'
sortWeight = 3000000
id = '93b107b5-afab-4cbd-9e9d-58a68cfe206e'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMzM4Mzg0LCJpYXQiOjE3NTEyNTE5ODQsImp0aSI6ImUzZDYzNGRhYTUyODRhZGNiNTJkZTE5MjQxOWY1NGVhIiwidXNlcl9pZCI6IjcxMmM2OTU1LTk3YmQtNDg3Mi1iN2NmLTgyMjUyODczMjIzMyJ9._mjZw9zEvkysVWWBsDLMPgCR0F-WnDe8iIcFT8UNWoE'

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
