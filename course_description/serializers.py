from course_description.models import CourseDescription


class CourseDescriptionSerializer:
    class Meta:
        model = CourseDescription
        fields = '__all__'

