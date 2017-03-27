# -*- coding:utf-8 -*-
class AuthRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'celery':
            return 'celery_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'celery':
            return 'celery_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'celery' or \
                        obj2._meta.app_label == 'celery':
            return True
        return None

    def allow_migrate(self, db, model):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if db == 'celery_db':
            return model._meta.app_label == 'celery'
        elif model._meta.app_label == 'celery':
            return False
        return None

    def allow_syncdb(self, db, model):

        if db == 'celery_db':
            return model._meta.app_label == 'celery'
        elif model._meta.app_label == 'celery':
            return False
        return None


class ProductsRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'products':
            return 'products_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'products':
            return 'products_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'products' or \
                        obj2._meta.app_label == 'products':
            return True
        return None

    def allow_migrate(self, db, model):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if db == 'products_db':
            return model._meta.app_label == 'products'
        elif model._meta.app_label == 'products':
            return False
        return None

    def allow_syncdb(self, db, model):

        if db == 'products_db':
            return model._meta.app_label == 'products'
        elif model._meta.app_label == 'products':
            return False
        return None

