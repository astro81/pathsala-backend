```toml
name = 'Rate Course'
description = '- Only for students'
method = 'POST'
url = '{{url}}/api/course-ratings/rate/73282e9a-11d8-4ff2-b9d6-9ccb10fd211f/'
sortWeight = 1000000
id = '4742a2a6-9317-4412-b099-d1a40eb55ced'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMzQwMjUxLCJpYXQiOjE3NTEyNTM4NTEsImp0aSI6IjdhMzI3NTczYThhYjQ2YTY4YmRmZjViMmRkODEwY2Q1IiwidXNlcl9pZCI6IjMyNmI5ODJkLTBlZTAtNDg0Ny04NTUzLTBkYzlmZGJjZmUwMiJ9.jPUBNxXj92ZKxO_WsSNAbZwvAVelBM2qmEniOfROxX4'

[body]
type = 'JSON'
raw = '''
{
  "rating": 5.0,
  "review": "Great introduction to Python!"
}'''
```
