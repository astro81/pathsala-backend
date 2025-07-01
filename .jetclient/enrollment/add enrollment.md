```toml
name = 'add enrollment'
method = 'POST'
url = '{{url}}/api/enrollment/addenrollment/'
sortWeight = 1000000
id = '5c7bb2ea-af5b-455d-bf26-7fa5efa2ae5e'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNDI1ODg2LCJpYXQiOjE3NTEzMzk0ODYsImp0aSI6IjUwMzIwMjRiNTBiNTQwNDdhYTlhYTUyNmNiMmM1NTg5IiwidXNlcl9pZCI6ImUxZTIyOGU0LTAyMDEtNDE4MC1iOWM4LTU0YzEyMTEyYjQ5MSJ9.5Kb6Uwu_oshxyU_aZIvs0wR6YbV3zwupfQwQX1Nbib4'

[body]
type = 'JSON'
raw = '''
{
  "course" : "536d0dbc-493a-4c91-ba77-a898071346bd",
  "user" : "e1e228e4-0201-4180-b9c8-54c12112b491",
 
}'''
```
