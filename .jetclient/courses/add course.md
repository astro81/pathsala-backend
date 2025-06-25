```toml
name = 'add course'
method = 'POST'
url = 'http://127.0.0.1:8000/api/courses/add-course/'
sortWeight = 2000000
id = '53c86376-5da4-4fe3-b68d-a794ee016325'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwODIxMjI2LCJpYXQiOjE3NTA4MjA5MjYsImp0aSI6IjFjN2E4MGM3Yjk0MDQ1MDdiZWZhZDg0YTg5NmYwNDAyIiwidXNlcl9pZCI6IjY4OGQzOWIzLWI2YzItNDU1MC1iOWMzLWQyZTIyZjM1YzFiNSJ9.8Rv02foYsOm4mzgzGpYsMyDg9gCeYW3tNQO05OQSXeM'

[body]
type = 'JSON'
raw = '''
{
  "name": "Django",
  "title": "Django developer",
  "duration": 45,
  "price": 3500,
  "rating": 3.88,
  "training_level": "intermediate",
  "class_type": "hybrid",
  "career_prospect": "A FUll fledged Django developer",
}'''
```
