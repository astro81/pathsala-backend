```toml
name = 'edit course'
method = 'PATCH'
url = 'http://127.0.0.1:8000/api/courses/edit-course/javascript-essentials/'
sortWeight = 4000000
id = 'b1e88c78-0712-4926-a3e4-7ec3973daf52'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwODQ3MjI0LCJpYXQiOjE3NTA4NDY5MjQsImp0aSI6IjcyYzFlNzY2Y2VlMzQ1Njk4YzA4OGNhODI1ZjNlZDIxIiwidXNlcl9pZCI6IjZkMjI5OTJkLTBkMDctNGZkMS1hMjdhLWIxOWY4ZGNhZGE0ZSJ9.fvNibrKEt_6QHVWtoKBuPRzuy4xPxJ-qfXrOSfInnZU'

[body]
type = 'JSON'
raw = '''
{
"description":{
  "course_introduction": "JS from scratch",
    "course_overview": "JS course covering basics to intermediate concepts",
    "course_requirements": "Need to know computer basics",
    "course_context": "Perfect for absolute beginners"
  }
}
   '''
```
