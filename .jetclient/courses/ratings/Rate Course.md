```toml
name = 'Rate Course'
description = '- Only for students'
method = 'POST'
url = '{{url}}/api/course-ratings/rate/536d0dbc-493a-4c91-ba77-a898071346bd/'
sortWeight = 1000000
id = '4742a2a6-9317-4412-b099-d1a40eb55ced'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMzc4MDg4LCJpYXQiOjE3NTEyOTE2ODgsImp0aSI6IjgyODIzMTg5NjEyYzQwMzdhZGIwOGY0YTEyMTc5YTZhIiwidXNlcl9pZCI6IjYzYmQwOTczLTRkMDMtNDRiZi1hZWZmLTMyNmU0MDA1ZDVhZCJ9.HWStoK5BjPYTjlJFUoc_BRN3UzorJBH1VDpEut1rwVs'

[body]
type = 'JSON'
raw = '''
{
  "rating": 4.9,
  "review": "Great introduction to Python!"
}'''
```
