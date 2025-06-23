```toml
name = 'edit self profile'
method = 'PUT'
url = 'http://localhost:8000/api/auth/user/edit/'
sortWeight = 5000000
id = '8c70fd9d-e004-4690-b0ad-8771f62b2591'

[[headers]]
key = 'Authorization'
value = 'Token 01ce1438ff02f572fb7bb7dc2952d120a36ec93d'

[body]
type = 'JSON'
raw = '''
{
  "id": "6119be9f-9f54-45fa-92c8-3022f6833176",
  "first_name": "Ashif",
  "last_name": "last",
  "email": "ashipaalam@gmail.com",
  "username": "aship444",
  "password": "securePass123",
  "password2": "securePass123",
  "last_login": "2025-06-23T03:41:31.630005Z",
  "date_joined": "2025-02-23T03:41:31.630005Z",
  "is_active": false
}
'''
```
