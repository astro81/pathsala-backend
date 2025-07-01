```toml
name = 'Rate Course'
description = '- Only for students'
method = 'POST'
url = '{{url}}/api/course-ratings/rate/bbf1e0b3-b83c-4cc7-9727-b95792bccffe/'
sortWeight = 1000000
id = '4742a2a6-9317-4412-b099-d1a40eb55ced'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNDI1MjkwLCJpYXQiOjE3NTEzMzg4OTAsImp0aSI6IjFmNTc5ZTcyZGUyMjQ5ZjVhN2Q5NGI5OWFlODVjNWMzIiwidXNlcl9pZCI6IjYzYmQwOTczLTRkMDMtNDRiZi1hZWZmLTMyNmU0MDA1ZDVhZCJ9.75_ha4w9jGNkrOwADoM-BtD83wyyXo44NbrMhFVNGTs'

[body]
type = 'JSON'
raw = '''
{
  "rating": 5.0,
  "review": "Great introduction to Python!"
}z'''
```
