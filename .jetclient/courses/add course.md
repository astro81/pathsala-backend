```toml
name = 'add course'
method = 'POST'
url = 'http://127.0.0.1:8000/api/courses/add-course/'
sortWeight = 2000000
id = '53c86376-5da4-4fe3-b68d-a794ee016325'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNzYzNjQ5LCJpYXQiOjE3NTA3NjMzNDksImp0aSI6Ijk1OGYzNTY1YjJmODRjMDU4M2ViN2NjYjZjMGRkMDhmIiwidXNlcl9pZCI6IjgyNTM3M2U2LWNiM2YtNGIwYS04NGE4LWZiZjg5MTMwM2ZiNCJ9.IhjOWW_wLO83qhYpPr39bGQgxd4UWDBgBWfGFUGIjAs'

[body]
type = 'JSON'
raw = '''
{
  "name": "Data Science",
  "title": "Data Analysis",
  "duration": 30,
  "price": 4000,
  "rating": 3.4,
  "training_level": "begginner",
  "class_type": "hybrid",
  "career_prospect": "A FUll fledged backend developer",
}'''
```
