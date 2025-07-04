```toml
name = 'add course'
description = '- Add a new course'
method = 'POST'
url = '{{url}}/api/courses/add/'
sortWeight = 1000000
id = '830c008d-0c3b-42a8-a662-0d5136589806'

[[headers]]
key = 'Authorization'
value = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNjg5MTE0LCJpYXQiOjE3NTE2MDI3MTQsImp0aSI6ImI1OTgwNjcxYTBlNTRlMDZiYTgyMWRiZDdiZTI0ZDI4IiwidXNlcl9pZCI6ImMzZWI5NjE1LTg2ODUtNDI1OC04ZDJmLWQ3MjMzZGI3MTJkNiJ9.zViTKJSdPDHK0ALIlvOHKpinspJW7S7YW7usirJ8Wp0'

[body]
type = 'JSON'
raw = '''
{
    "name": "React",
    "title": " JS Framework",
    "duration_weeks": 8,
    "price": "15000.00",
    "training_level": "advanced",
    "class_type": "online",
    "categories": ["Web Dev", "Backend"],
    "overview": "Learn the fundamentals of Python programming language from scratch.",
    "objectives": [
        "Understand basic Python syntax",
        "Learn about variables and data types",
        "Master control flow statements",
        "Write simple Python programs"
    ],
    "prerequisites": [
        "Basic computer literacy",
        "No prior programming experience required"
    ],
    "outcomes": [
        "Ability to write Python scripts",
        "Understanding of core programming concepts",
        "Foundation for advanced Python topics"
    ],
    "curriculum": [
        {
            "week": 1,
            "title": "Introduction to Python",
            "topics": ["Installation", "Syntax basics", "Variables"]
        },
        {
            "week": 2,
            "title": "Control Flow",
            "topics": ["Conditionals", "Loops", "Functions"]
        }
    ]
}'''
```
