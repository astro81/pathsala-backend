```toml
name = 'Register Moderator'
description = '- Only Admin can create a moderator'
method = 'POST'
url = '{{url}}/api/auth/register/moderator/'
sortWeight = 3000000
id = '93b107b5-afab-4cbd-9e9d-58a68cfe206e'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMjAyMzQ4LCJpYXQiOjE3NTExMTU5NDgsImp0aSI6IjVlNWQ4MTI4Mzc1NzQ3ODQ4NGE5Nzc5N2U0MWFjYWRiIiwidXNlcl9pZCI6ImI4ZjVlOTZhLTI1ZDgtNDEyMS1hNTRiLTIxNzIyNzVlMTRkZCJ9.Cy2Vqy1TEVVh71Otns60Kmex_2lB9qrVwIHWHDFXMpc'

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
