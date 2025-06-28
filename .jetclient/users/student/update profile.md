```toml
name = 'update profile'
description = '- partially update the student details '
method = 'PATCH'
url = '{{url}}/api/auth/update/student/profile/'
sortWeight = 6000000
id = 'f6e20d8a-8c77-4dda-bb80-7a00874b77ce'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMjAwNzQ5LCJpYXQiOjE3NTExMTQzNDksImp0aSI6ImYzNDY4M2VjNjBjMTQ5ZDViODVmYTU5ZTE2ZDNmZmIzIiwidXNlcl9pZCI6IjkyOTg0NDRjLTZkZTAtNDQ0Yi05MTU4LWRlNDM1YWNlNTRiYSJ9.F-x5OrIj551keTmwigrh3N34MiA5vV7TyctKY7NADKA'

[body]
type = 'JSON'
raw = '''
{
    "first_name": "John"
}'''
```
