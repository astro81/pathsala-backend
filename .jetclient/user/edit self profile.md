```toml
name = 'edit self profile'
method = 'PATCH'
url = 'http://localhost:8000/api/auth/user/edit/'
sortWeight = 5000000
id = '8c70fd9d-e004-4690-b0ad-8771f62b2591'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNzM3Njk1LCJpYXQiOjE3NTA3MzczOTUsImp0aSI6Ijg2Njg4NjUyM2ZlMzQ4NmU5ODQyZWY3NmY0OTc4YWQyIiwidXNlcl9pZCI6IjI1NWJhZTgzLWM1MDEtNDAzOS05ZTEwLWE2ODVmZDc0ZjY4YSJ9.Xqyfz-UKSGOqrMegivMw7JvnaV7lS_5znPcW7gAltvM'

[body]
type = 'JSON'
raw = '''
{
  "id": "6119be9f-9f54-45fa-92c8-3022f6833176",
  "first_name": "ACERRR",
  "last_name": "okk",
  "email": "aship100@gmail.com",
  "username": "aship100",
  "password": "securePass@321",
  "password2": "securePass@321",
  "last_login": "2025-06-23T03:41:31.630005Z",
  "date_joined": "2025-02-23T03:41:31.630005Z",
  "is_active": false
}
'''
```
