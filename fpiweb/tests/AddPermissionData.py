# Generated by Django 3.0.8 on 2020-07-30 00:27

import os
from typing import Dict, List
from sys import stderr

from django.apps import apps
from django.core.management import ManagementUtility
from django.db import migrations

GROUPS_AND_PERMISSIONS: Dict[str, Dict[str, Dict[str, List[str]]]] = {
    'Volunteer': {
        'fpiweb': {
            'box': [
                'add_box',
                'check_in_box',
                'check_out_box',
                'move_box',
                'view_box'
            ],
            'pallet': [
                'build_pallet',
                'move_pallet',
                'view_pallet',
            ],
        },
    },
    'Staff': {
        'fpiweb': {
            'activity': [
                'view_activity',
            ],
        'box': [
            'print_labels_box',
        ],
        'constraints': [
            'add_constraints',
            'change_constraints',
            'delete_constraints',
            'view_constraints',
        ],
        'locbin': [
            'add_locbin',
            'change_locbin',
            'delete_locbin',
            'view_locbin',
        ],
        'locrow': [
            'add_locrow',
            'change_locrow',
            'delete_locrow',
            'view_locrow',
        ],
        'loctier': [
            'add_loctier',
            'change_loctier',
            'delete_loctier',
            'view_loctier',
        ], 'profile': [
                'view_system_maintenance',
            ],
        },
    },
    'Admin': {
        'fpiweb': {
            'profile': [
                'view_system_maintenance',
            ],
        }
    }
}


def iterate_permissions(permissions):
    """
    Generator to pick up the needed foreign keys for a given permisison.

    :param permissions: attributes associated with this permission
    :return:
    """
    for app_label, models in permissions.items():
        for model, model_permissions in models.items():
            for permission in model_permissions:
                yield app_label, model, permission


def setup_group_permissions(group, permissions):
    """
    For a given group, create or replace the permisisons for it.

    :param group: group to be created or replaced
    :param permissions: list of permissions to be applied to this group
    :return:
    """
    # Establish the correct historical models for the auth tables.
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    print(f"Clearing {group.name} permissions.")
    group.permissions.clear()


    for app_label, model, codename in iterate_permissions(permissions):
        try:
            permission = Permission.objects.get(
                content_type__app_label=app_label, content_type__model=model,
                codename=codename)
        except Permission.DoesNotExist:
            print(f"Permission {model} {codename} not found", file=stderr)
            continue

        print(f"Granting {model} {codename} to {group.name}")
        group.permissions.add(permission)


def setup_groups_and_permissions(*args, **kwargs):
    """
    Create or replace groups and add permissions.

    :param groups_and_permissions: table of groups and associated permissions
    :return:
    """
    # first ensure that the content types have been built for our app and
    # for auth by sumulating a call to a django_extensions module
    print('Verifying that prevously defined permissions are in place...')
    mu = ManagementUtility()
    argv = (
        'manage.py',                   # simulated calling module
        'update_permissions',          # django_extensions subcommand
        '--apps', 'fpiweb,auth',       # parameters to fix these apps
        '--verbosity', '3',            # ask it to tell us what it did
    )
    print('Verification finished\n')

    # Establish the correct historical models for the auth tables.
    Group = apps.get_model('auth', 'Group')

    # Establish data needed by this function
    groups_and_permissions = GROUPS_AND_PERMISSIONS

    for group_name, permissions in groups_and_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Created {group_name} group.")
        else:
            print(f"Found {group_name} group.")

        setup_group_permissions(group, permissions)
        print()


if __name__ == '__main__':
    # Boilerplate for stand-alone Django scripts
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FPIDjango.settings')

    from django import setup
    setup()

    from django.contrib.auth.models import Group, Permission


    # run application
    setup_groups_and_permissions()
