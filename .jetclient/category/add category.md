```toml
name = 'add category'
method = 'POST'
url = '{{url}}/api/category/add-category/'
sortWeight = 1000000
id = 'a561f2b0-bafd-4994-9ab5-321b7353cb9b'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMDIxNzEwLCJpYXQiOjE3NTEwMjE0MTAsImp0aSI6IjIzMmRjNjc0NTk0ZjQ2MjFiMTMyNWNhNzYzZjNmOTQwIiwidXNlcl9pZCI6IjU5ZjdiYTM4LTk4NDgtNDFjMC1hYWE3LWVkOGVkOTg2ODAxNSJ9.9OWLxgwnAYz85YY3nGnfsa2ttT4Gic5UgH9GCoF6Z8k'

[body]
type = 'JSON'
raw = '''
{
  "name": "Full Development"
}'''
```
