```toml
name = 'add category'
method = 'POST'
url = '{{url}}/api/category/add-category/'
sortWeight = 1000000
id = 'a561f2b0-bafd-4994-9ab5-321b7353cb9b'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwOTE2NzIxLCJpYXQiOjE3NTA5MTY0MjEsImp0aSI6ImQ5NzIzMGEzOWU0NzRlOTFiNjAyMzdmMzllNTAxMGY1IiwidXNlcl9pZCI6IjI1MDk4YzBhLWNmNjQtNDVhNi04YTBjLTEzYzExMjQ0MzhkYyJ9.0jNTkAkerbW5y72KqUVvhdu0t59B7G4fT7jdp0w4lWo'

[body]
type = 'JSON'
raw = '''
{
  "name": "Full Development"
}'''
```
