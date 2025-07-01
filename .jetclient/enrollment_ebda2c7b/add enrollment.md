```toml
name = 'add enrollment'
method = 'POST'
url = '{{url}}/api/enrollment/addenrollment/'
sortWeight = 1000000
id = '5dc2cf32-9658-45b2-b311-1684c4024bb8'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNDI5OTkzLCJpYXQiOjE3NTEzNDM1OTMsImp0aSI6ImUxZGY2YzU2NjU2MTQxYjliYzY2YzBiNjZkZDFkZDVjIiwidXNlcl9pZCI6IjUxYjFmOTY4LWUyNjQtNDJhZi04MjFiLWQ4YTc1MDJlMTNkNCJ9.UBupzodd3MJalI0W_WO0FxYiCayK48sv41usAPngvwI'

[body]
type = 'JSON'
raw = '''
{
  "course" : "d5ead67d-8af6-475e-ba64-988b303225bf",
  "user" : "63bd0973-4d03-44bf-aeff-326e4005d5ad"
}'''
```
