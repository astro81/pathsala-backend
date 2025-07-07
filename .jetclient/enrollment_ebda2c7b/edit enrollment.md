```toml
name = 'edit enrollment'
method = 'PATCH'
url = '{{url}}/api/enrollment/editenrollment/ff90d434-4b97-4b4e-8163-6557e9b54640/'
sortWeight = 3000000
id = 'e39303c4-2ae0-42c6-b462-37d02e61dd2f'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxOTQ5MDA1LCJpYXQiOjE3NTE4NjI2MDUsImp0aSI6IjhlOGE1NDI2OTI0NDQwMWY5MjA4ZmE0N2QyNzhiNTVkIiwidXNlcl9pZCI6ImYxZDUwMTQ2LWUyZjQtNDY1NC1iNzhjLTUxNGQ0OWUyODgyYyJ9.xFliir6rylbpPzgexWaslQm73qYZBnKoYbYDFgaGUOs'

[body]
type = 'JSON'
raw = '''
{
  "status" : "approved",
  "payment" : "paid",
}'''
```
