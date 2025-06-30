```toml
name = 'edit enrollement'
method = 'PATCH'
url = '{{url}}/api/enrollment/editenrollment/5e35ecd7-8ccc-4b3e-932b-fb7d51d7b22d/'
sortWeight = 4000000
id = '96416c43-b8de-4aad-a75c-327663726412'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMzcyNDk5LCJpYXQiOjE3NTEyODYwOTksImp0aSI6ImMxZGQzMjAwZTMwNzQ0NjA4OTZjODQwMDM3OTU3NTAzIiwidXNlcl9pZCI6Ijc0NTRkMjg5LTRmZjQtNGVmYS05OTAxLTQ1ZGI3MzJjYzQzNCJ9.TMvlP57oA7V4cD3jd8doebk95pqxsw9yMedfFy19fTw'

[body]
type = 'JSON'
raw = '''
{
  "approved_by" : "moderator",
  "status": "pending"
}'''
```
