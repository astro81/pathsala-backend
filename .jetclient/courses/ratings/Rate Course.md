```toml
name = 'Rate Course'
description = '- Only for students'
method = 'POST'
url = '{{url}}/api/course-ratings/rate/d5ead67d-8af6-475e-ba64-988b303225bf/'
sortWeight = 1000000
id = '4742a2a6-9317-4412-b099-d1a40eb55ced'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNDI5OTkzLCJpYXQiOjE3NTEzNDM1OTMsImp0aSI6ImUxZGY2YzU2NjU2MTQxYjliYzY2YzBiNjZkZDFkZDVjIiwidXNlcl9pZCI6IjUxYjFmOTY4LWUyNjQtNDJhZi04MjFiLWQ4YTc1MDJlMTNkNCJ9.UBupzodd3MJalI0W_WO0FxYiCayK48sv41usAPngvwI'

[body]
type = 'JSON'
raw = '''
{
  "rating": 3.9,
  "review": "Awesome Course Content"
}'''
```
