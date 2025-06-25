```toml
name = 'create moderator (only admin)'
method = 'POST'
url = 'http://localhost:8000/api/auth/create-moderator/'
sortWeight = 7000000
id = 'd4c0ed78-15f8-43f3-9a59-6a219f0dc805'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwODU1NjkxLCJpYXQiOjE3NTA4NTUzOTEsImp0aSI6IjhmNGQxNDc5Y2M1YzQ5ZmFhN2QwM2Q4OGUyN2RjNzI5IiwidXNlcl9pZCI6IjlkMzVhZGUwLTkwMTItNGM4Ni1iNjFiLWJkNjE3N2E0ZWEzYyJ9.EFVoB6WI1_gL_zV5rLlchwdxKBk4f7WjKgq2mF5yZnc'

[body]
type = 'JSON'
raw = '''
{
  "username": "moderator",
  "email": "moderator@example.com",
  "password": "Mod@1234",
  "password2": "Mod@1234"
}
'''
```
