```toml
name = 'add enrollment'
method = 'POST'
url = '{{url}}/api/enrollment/addenrollment/'
sortWeight = 1000000
id = '5dc2cf32-9658-45b2-b311-1684c4024bb8'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUyMzM3MzcxLCJpYXQiOjE3NTIyNTA5NzEsImp0aSI6IjZjM2VlMjQxOWIzNjQzYTBhNzdkYzNiOWFiMzI5ZmU3IiwidXNlcl9pZCI6IjMwN2ZlMDVjLTE1YjMtNDYwMC1iZjFiLTkxNDhhYjg5OTk3OSJ9.ujuP3JwLeeCpHbPEpRQFF1SjVgjzi6plL4MN-Icqsso'

[body]
type = 'JSON'
raw = '''
{
  "course_id" : "24759f66-8be2-4cee-8562-cfd2f5be05a2",
  "fullName" : "Acer Nitro",
  "email" : "nitro123@gmail.com",
  "whatsApp" : "9876543210",
  
}'''
```
