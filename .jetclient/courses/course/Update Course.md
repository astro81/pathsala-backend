```toml
name = 'Update Course'
description = '- Update a prexisting course'
method = 'PATCH'
url = '{{url}}/api/courses/update/python-intermidate/'
sortWeight = 3000000
id = 'a2a88939-7759-49f5-8a4c-3a9f1803cfb7'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMzY3NjAyLCJpYXQiOjE3NTEyODEyMDIsImp0aSI6IjM0N2U3ZGRiODE5YTQ5YTk5YzE1ZDVhYzQyODAwNTYwIiwidXNlcl9pZCI6ImMzZWI5NjE1LTg2ODUtNDI1OC04ZDJmLWQ3MjMzZGI3MTJkNiJ9.nOOsRyA42Xgu5hCL7NFInmo9ZsYNEZm-PEAV-XM6vow'

[body]
type = 'JSON'
raw = '''
{
  "price": 500,
     "categories_input": ["New Category 1", "New Category 2"]
}'''
```
