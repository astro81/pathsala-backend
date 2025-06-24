```toml
name = 'edit course'
method = 'PATCH'
url = 'http://127.0.0.1:8000/api/courses/edit-course/Python/'
sortWeight = 4000000
id = 'b1e88c78-0712-4926-a3e4-7ec3973daf52'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNzc2Nzc3LCJpYXQiOjE3NTA3NzY0NzcsImp0aSI6ImFlYWQ5OGY5MTMwOTQ3OGQ4YWFhM2ZmODk0MDA5ODExIiwidXNlcl9pZCI6IjY4OGQzOWIzLWI2YzItNDU1MC1iOWMzLWQyZTIyZjM1YzFiNSJ9.yAoE9DkydivEVKKCzRa7TfQxzTRgAfmaI743curqKEY'

[body]
type = 'JSON'
raw = '''
{
  "id": "d75a4b50-1b5b-4e06-96ee-5b49822137bb",
  "name": "Django",
  "title": "Python with django developer",
  "duration": "00:00:30",
  "price": "4000.00",
  "rating": "3.40",
  "training_level": "beginner",
  "class_type": "offline",
  "career_prospect": "A FUll fledged backend developer",
}
   '''
```
