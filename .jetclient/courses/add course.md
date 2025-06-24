```toml
name = 'add course'
method = 'POST'
url = 'http://127.0.0.1:8000/api/courses/add-course/'
sortWeight = 2000000
id = '53c86376-5da4-4fe3-b68d-a794ee016325'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNzgwOTg3LCJpYXQiOjE3NTA3ODA2ODcsImp0aSI6ImZjNDc5ZTNkMDdlZDQzZjRhN2M4YmU0ZTA2NjBhMzhjIiwidXNlcl9pZCI6IjY4OGQzOWIzLWI2YzItNDU1MC1iOWMzLWQyZTIyZjM1YzFiNSJ9.8s0w2V5VTnso24cDLW56t_gatx7_Oa3-joPBClqFU6E'

[body]
type = 'JSON'
raw = '''
{
  "name": "Python",
  "title": "Python developer",
  "duration": 30,
  "price": 4000,
  "rating": 3.4,
  "training_level": "beginner",
  "class_type": "hybrid",
  "career_prospect": "A FUll fledged backend developer",
}'''
```
