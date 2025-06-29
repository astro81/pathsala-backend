```toml
name = 'add enrollment'
method = 'POST'
url = '{{url}}/api/enrollment/addenrollmemt/'
sortWeight = 1000000
id = '5c7bb2ea-af5b-455d-bf26-7fa5efa2ae5e'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMzAzNTg5LCJpYXQiOjE3NTEyMTcxODksImp0aSI6Ijg5ZmE5YzA4MWViYjQyMzA4ZDU2NzhlOGQyM2U3NTA0IiwidXNlcl9pZCI6IjA2ZmFjYjNhLWM3MzAtNDIzZi05Yzg3LWE4MjAzMTI3ZWZjOCJ9.aQXo9viB0wcwVuMP3veJRlmjT-U6cvA8yNPU1-R7ae8'

[body]
type = 'JSON'
raw = '''
{
  "course" : "devops-engineering-2024"
}'''
```
