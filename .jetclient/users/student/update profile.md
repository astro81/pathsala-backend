```toml
name = 'update profile'
description = '- partially update the student details '
method = 'PATCH'
url = '{{url}}/api/auth/update/student/profile/'
sortWeight = 6000000
id = 'f6e20d8a-8c77-4dda-bb80-7a00874b77ce'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMjU3MzY3LCJpYXQiOjE3NTExNzA5NjcsImp0aSI6IjA4MGRkMmI1OWM1YjQ0NjY4YjhjZTdhMDU0NDQ0YTlkIiwidXNlcl9pZCI6ImY0ZDQ2YzkwLTc0ODAtNGQzOS04NTQ0LTdkNjllOGY5OTIwZSJ9.N4_T8qnHKQQxCvEN2o2h1rHPG1kLVUzTyNpBMmkZxHU'

[body]
type = 'JSON'
raw = '''
{
    "first_name": "Jo"
}'''
```
