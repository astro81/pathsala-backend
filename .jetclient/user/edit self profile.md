```toml
name = 'edit self profile'
method = 'PUT'
url = 'http://localhost:8000/api/auth/user/edit/'
sortWeight = 5000000
id = '8c70fd9d-e004-4690-b0ad-8771f62b2591'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNjkwMTMzLCJpYXQiOjE3NTA2ODk4MzMsImp0aSI6IjgyYWUxMTIxMzhiNDQxNDdhMjA1YjdiMWZkYTE3MzNlIiwidXNlcl9pZCI6IjdjY2FiZDIwLTllNzgtNGVlZi1hMTNmLTA0NWUxMTkyOGIwNSJ9.NTun1NWMWkHtom5XPGUe40FwVHcX_4yYyZTozDCXRGc'

[body]
type = 'JSON'
raw = '''
{
  "id": "6119be9f-9f54-45fa-92c8-3022f6833176",
  "first_name": "Ashif",
  "last_name": "okk",
  "email": "ashipaalam@gmail.com",
  "username": "aship444",
  "password": "securePass@123",
  "password2": "securePass@123",
  "last_login": "2025-06-23T03:41:31.630005Z",
  "date_joined": "2025-02-23T03:41:31.630005Z",
  "is_active": false
}
'''
```
