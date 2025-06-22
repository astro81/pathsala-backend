```toml
name = 'create moderator (only admin)'
method = 'POST'
url = 'http://localhost:8000/api/auth/create-moderator/'
sortWeight = 7000000
id = 'd4c0ed78-15f8-43f3-9a59-6a219f0dc805'

[[headers]]
key = 'Authorization'
value = 'Token 4498fbfab0d9141229112206e29f4b3478075fe4'

[body]
type = 'JSON'
raw = '''
{
  "username": "moderator_user",
  "email": "mod@example.com",
  "password": "moderator123",
  "password2": "moderator123"
}
'''
```
