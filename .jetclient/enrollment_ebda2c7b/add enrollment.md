```toml
name = 'add enrollment'
method = 'POST'
url = '{{url}}/api/enrollment/addenrollment/'
sortWeight = 1000000
id = '5dc2cf32-9658-45b2-b311-1684c4024bb8'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNzYwMDYxLCJpYXQiOjE3NTE2NzM2NjEsImp0aSI6IjI0NWUyNmYzNjY0MjRmMTM4Y2UyNjZlMzgwY2M4ZjBlIiwidXNlcl9pZCI6IjY0MTBkNmY1LTViZTYtNGEzOC1hYTI4LTBmNzhlZmUwZDE5YSJ9.4rOscoo1pQZu-AqpKdUU8yF9WHL8ZjQOqhHepWZ5Xw4'

[body]
type = 'JSON'
raw = '''
{
  "course" : "65c94f96-5882-4fa5-bbcf-8485be787c39",
  "fullName" : "Aship Aalam",
  "email" : "aship@Student.com",
  "whatsApp" : "9876543210",
  
}'''
```
