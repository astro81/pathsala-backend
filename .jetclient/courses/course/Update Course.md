```toml
name = 'Update Course'
description = '- Update a prexisting course'
method = 'PATCH'
url = '{{url}}/api/courses/update/python-intermidate/'
sortWeight = 3000000
id = 'a2a88939-7759-49f5-8a4c-3a9f1803cfb7'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMzQwMjE1LCJpYXQiOjE3NTEyNTM4MTUsImp0aSI6IjlhZjVhZWFmYzk5ZDRmMjI5ZjhkMWFiZTcwYjAzMzhjIiwidXNlcl9pZCI6ImYzMGM0MzZkLTY3MGUtNGJjMy1hMmU4LWZkMWU4YmJlYWZmOSJ9.dIL5uLdkl9ezjeLOa8_orwUqEzNVbPFO5ncPb6hlvvE'

[body]
type = 'JSON'
raw = '''
{
  "price": 500,
  "categories_input": ["New Category 1", "New Category 2"]
}'''
```
