from rolepermissions.roles import AbstractUserRole

class Admin(AbstractUserRole):
    available_permissions = {
        'view_course': True,
        'add_course': True,
        'edit_course': True,
        'delete_course': True,
        'manage_users': True,
    }

class Moderator(AbstractUserRole):
    available_permissions = {
        'view_course': True,
        'add_course': True,
        'edit_course': True,
    }

class Student(AbstractUserRole):
    available_permissions = {
        'view_course': True,
    }

