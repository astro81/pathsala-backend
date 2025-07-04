```toml
name = 'Rate Course'
description = '- Only for students'
method = 'POST'
url = '{{url}}/api/course-ratings/rate/d5ead67d-8af6-475e-ba64-988b303225bf/'
sortWeight = 1000000
id = '4742a2a6-9317-4412-b099-d1a40eb55ced'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNjAzNjIwLCJpYXQiOjE3NTE1MTcyMjAsImp0aSI6IjFiOTAzNDkwNDcwMjRjNDU5YmEzNGY1YmQ1ODQ2MGM1IiwidXNlcl9pZCI6IjYzYmQwOTczLTRkMDMtNDRiZi1hZWZmLTMyNmU0MDA1ZDVhZCJ9.racOSIaSa5CAQo9Zte0S7PHb_9O2HxV2duobVSsCBKw'

[body]
type = 'JSON'
raw = '''
{
  "rating": 3.9,
  "review": "Awesome Course Content"
}'''
```
