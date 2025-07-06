```toml
name = 'list courses'
description = '- List of all of the courses'
method = 'GET'
url = '{{url}}/api/courses/list/?average_rating__gte=1.5'
sortWeight = 2000000
id = 'cd4b2054-5030-413b-8b32-722122e28833'

[[queryParams]]
key = 'average_rating__gte'
value = '1.5'
```
