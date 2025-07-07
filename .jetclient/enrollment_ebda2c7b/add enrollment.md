```toml
name = 'add enrollment'
method = 'POST'
url = '{{url}}/api/enrollment/addenrollment/'
sortWeight = 1000000
id = '5dc2cf32-9658-45b2-b311-1684c4024bb8'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxOTQ5OTQwLCJpYXQiOjE3NTE4NjM1NDAsImp0aSI6IjMzYTdhMTRkYjAyMTQ0NThiM2QyZDhlOTQxNDZmOTIxIiwidXNlcl9pZCI6ImM1YThmY2FkLTViNTQtNGFhZC05NTQ2LTcwODRmOGZhNTU5MCJ9.yyJDf8KGYSdOCsZ00A-bRQuz38lylHj4t35CK926RZI'

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
