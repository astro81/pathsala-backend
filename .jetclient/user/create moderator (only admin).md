```toml
name = 'create moderator (only admin)'
method = 'POST'
url = 'http://localhost:8000/api/auth/create-moderator/'
sortWeight = 7000000
id = 'd4c0ed78-15f8-43f3-9a59-6a219f0dc805'

[[headers]]
key = 'Authorization'
value = 'Token 8c6a53b8e088fa58c1fe4d637b5e7d6f05f90d12'

[body]
type = 'JSON'
raw = '''
{
  "username": "moderator_User",
  "email": "moderator_User@example.com",
  "password": "adminpassword",
  "password2": "adminpassword"
}
'''
```
