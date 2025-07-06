```toml
name = 'Update Course'
description = '- Update a prexisting course'
method = 'PATCH'
url = '{{url}}/api/courses/update/linux/'
sortWeight = 3000000
id = 'a2a88939-7759-49f5-8a4c-3a9f1803cfb7'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxODYyMzQxLCJpYXQiOjE3NTE3NzU5NDEsImp0aSI6ImE0ZWQ0Y2JkN2U2YTRhYTE5YWVjMGYyODM3NTgwM2QyIiwidXNlcl9pZCI6ImY0OWY4NjhhLTViYmMtNGE3Mi04MjY2LTBhMjA4OGQ0ZDI4MCJ9.m2fx39SLLrVx22hfcddR-LP0bMyJW-yv-xk7kz4T8sE'

[body]
type = 'JSON'
raw = '''
{
    "categories": ["dev"]
}'''
```
