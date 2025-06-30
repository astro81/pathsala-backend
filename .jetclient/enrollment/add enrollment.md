```toml
name = 'add enrollment'
method = 'POST'
url = '{{url}}/api/enrollment/addenrollment/'
sortWeight = 1000000
id = '5c7bb2ea-af5b-455d-bf26-7fa5efa2ae5e'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMzY2NTAyLCJpYXQiOjE3NTEyODAxMDIsImp0aSI6ImZjZjdkMTQyOTQ5ZDRjYjU4YWVlMjkyZWU2MTU2N2M2IiwidXNlcl9pZCI6ImU0OGU5Mzc5LTY2N2QtNDcwZS04NGMwLTFiNzJiNWU0M2IyZCJ9.dxFklI-aeFcT9m4gwUJ5EVqCb6VHGkOt8-7pcvnRDio'

[body]
type = 'JSON'
raw = '''
{
  "course" : "1506a09d-9879-47cb-be9d-db281baa9639",
  "user" : "fc606c65-ad6f-488e-af27-ca656dba12b8",
 
}'''
```
