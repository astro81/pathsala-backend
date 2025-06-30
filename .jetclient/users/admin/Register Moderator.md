```toml
name = 'Register Moderator'
description = '- Only Admin can create a moderator'
method = 'POST'
url = '{{url}}/api/auth/register/moderator/'
sortWeight = 3000000
id = '93b107b5-afab-4cbd-9e9d-58a68cfe206e'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMzY2NDMxLCJpYXQiOjE3NTEyODAwMzEsImp0aSI6ImEwYzI0ODg3NThkYzQ2YjQ4OGJkNjQ1NDYwOTg0MGJiIiwidXNlcl9pZCI6Ijc0NTRkMjg5LTRmZjQtNGVmYS05OTAxLTQ1ZGI3MzJjYzQzNCJ9.W_qkDU6UZLOyoSJWyVfqQF0RQeOd0fgX_fGMW2z3bGs'

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
