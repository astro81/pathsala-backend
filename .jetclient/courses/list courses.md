```toml
name = 'list courses'
method = 'GET'
url = 'http://127.0.0.1:8000/api/courses/list-courses/'
sortWeight = 1000000
id = '91a82eae-1d77-4769-974d-30a6ca416a21'

[[queryParams]]
key = 'training_level'
value = 'advanced'
disabled = true

[[queryParams]]
key = 'class_type'
value = 'offline'
disabled = true

[[queryParams]]
key = 'duration'
value = '60'
disabled = true
```
