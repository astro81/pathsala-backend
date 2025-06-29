```toml
name = 'delete profile'
description = '- users can delete their own profile'
method = 'DELETE'
url = '{{url}}/api/auth/user/delete/'
sortWeight = 7000000
id = 'e4ddc6b1-3080-4a62-9dc1-c5ff51fa7ff4'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMjU3MzY3LCJpYXQiOjE3NTExNzA5NjcsImp0aSI6IjA4MGRkMmI1OWM1YjQ0NjY4YjhjZTdhMDU0NDQ0YTlkIiwidXNlcl9pZCI6ImY0ZDQ2YzkwLTc0ODAtNGQzOS04NTQ0LTdkNjllOGY5OTIwZSJ9.N4_T8qnHKQQxCvEN2o2h1rHPG1kLVUzTyNpBMmkZxHU'

[body]
type = 'JSON'
raw = '''
{
  "username": "test",
  "password": "StrongPass!23"
}'''
```
