"""
Role Definitions for django-role-permissions

This module defines the application's roles and their associated permissions using
django-role-permissions' AbstractUserRole. Each role specifies exactly what actions
its members are authorized to perform.

Roles:
    Admin: System administrators with full privileges
    Moderator: Content moderators with limited management rights
    Student: Regular users with read-only access

The permission system follows the principle of the least privilege, granting only
the necessary permissions for each role to perform its duties.
"""

from rolepermissions.roles import AbstractUserRole


class Admin(AbstractUserRole):
    """System Administrator Role with full privileges.

    Admins have unrestricted access to all platform features including
    - Complete course management (CRUD operations)
    - Category management
    - User administration

    Permissions
    ----------
    view_course : bool
        Can view all courses
    add_course : bool
        Can create new courses
    edit_course : bool
        Can modify existing courses
    delete_course : bool
        Can remove courses
    add_category : bool
        Can create new categories
    edit_category : bool
        Can modify existing categories
    delete_category : bool
        Can remove categories
    manage_users : bool
        Can administer user accounts and roles

    Example
    -------
    >>> from rolepermissions.roles import assign_role
    >>> assign_role(user, Admin)
    """

    available_permissions = {
        'view_course': True,
        'add_course': True,
        'edit_course': True,
        'delete_course': True,
        'add_category': True,
        'edit_category': True,
        'delete_category': True,
        'manage_users': True,
    }


class Moderator(AbstractUserRole):
    """Content Moderator Role with limited management rights.

    Moderators can manage course content but cannot:
    - Delete any content
    - Manage user accounts
    - Modify system categories

    Permissions
    ----------
    view_course : bool
        Can view all courses
    add_course : bool
        Can create new courses
    edit_course : bool
        Can modify existing courses
    add_category : bool
        Can create new categories
    edit_category : bool
        Can modify existing categories

    Example
    -------
    >>> from rolepermissions.roles import assign_role
    >>> assign_role(user, Moderator)
    """

    available_permissions = {
        'view_course': True,
        'add_course': True,
        'edit_course': True,
        'add_category': True,
        'edit_category': True,
    }


class Student(AbstractUserRole):
    """Platform User Role with read-only access.

    Students can:
    - View available courses
    Cannot:
    - Modify any content
    - Access administrative features

    Permissions
    ----------
    view_course : bool
        Can view available courses

    Example
    -------
    >>> from rolepermissions.roles import assign_role
    >>> assign_role(user, Student)
    """

    available_permissions = {
        'view_course': True,
        'rate_course': True,
    }

