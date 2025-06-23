from rolepermissions.roles import AbstractUserRole


class Admin(AbstractUserRole):
    """
    Role: Admin

    Admin users have full access to manage courses and users.
    They are the highest authority and can perform all operations,
    including viewing, adding, editing, and deleting courses, as well as managing users.
    """
    available_permissions = {
        'view_course': True,
        'add_course': True,
        'edit_course': True,
        'delete_course': True,
        'manage_users': True,
    }


class Moderator(AbstractUserRole):
    """
    Role: Moderator

    Moderators assist in managing course content but do not have user management rights.
    They can view, add, and edit courses, but cannot delete them or manage users.
    """
    available_permissions = {
        'view_course': True,
        'add_course': True,
        'edit_course': True,
    }


class Student(AbstractUserRole):
    """
    Role: Student

    Students are the end users of the platform.
    They only have permission to view courses and are not allowed to modify any data.
    """
    available_permissions = {
        'view_course': True,
    }
