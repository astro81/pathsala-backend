```toml
name = 'create moderator (only admin)'
method = 'POST'
url = 'http://localhost:8000/api/auth/create-moderator/'
sortWeight = 7000000
id = 'd4c0ed78-15f8-43f3-9a59-6a219f0dc805'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNzQxMTk5LCJpYXQiOjE3NTA3NDA4OTksImp0aSI6ImVkNDUxN2Q0NTMyZTQ3YzhhMTIwODQwOWU3NzRkNzlkIiwidXNlcl9pZCI6IjY4OGQzOWIzLWI2YzItNDU1MC1iOWMzLWQyZTIyZjM1YzFiNSJ9.Z-yNBuY7vuMP2EkO3y6e5G8M62v2I9nB9q9p1Ai-4HQ'

[body]
type = 'JSON'
raw = '''
{
  "username": "moderator_User",
  "email": "moderator_User@example.com",
  "password": "Adminpassword1@",
  "password2": "Adminpassword1@"
}
'''
```
