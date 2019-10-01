"""

This file declares the PCA interfaces and their methods:

This code is based on CKAN 
:Copyright (C) 2007 Open Knowledge Foundation
:license: AGPL V3, see LICENSE for more details.

"""


__all__ = [
    "Interface",
    "IRoutes",
    "IConfig",
    "IResource",
    "IPluginObserver",
    "IPluralize",
    "ISchema",
    "IDatabase",
    "IAuthorize",
]


from inspect import isclass
from pyutilib.component.core import Interface as _pca_Interface


class Interface(_pca_Interface):
    @classmethod
    def provided_by(cls, instance):
        return cls.implemented_by(instance.__class__)

    @classmethod
    def implemented_by(cls, other):
        if not isclass(other):
            raise TypeError("Class expected", other)
        try:
            return cls in other._implements
        except AttributeError:
            return False


class IRoutes(Interface):
    """
    Plugin into the creation of routes.

    """

    def before_mapping(self, config):
        """
        Called before the mapping of routes made by ushauri.

        :param config: ``pyramid.config`` object
        :return Returns a dict array [{'name':'myroute','path':'/myroute','view',viewDefinition,'renderer':'renderere_used'}]
        """
        return []

    def after_mapping(self, config):
        """
        Called after the mapping of routes made by ushauri.

        :param config: ``pyramid.config`` object
        :return Returns a dict array [{'name':'myroute','path':'/myroute','view',viewDefinition,'renderer':'renderere_used'}]
        """
        return []


class IConfig(Interface):
    """
    Allows the modification of the Pyramid config. For example to add new templates or static directories
    """

    def update_config(self, config):
        """
        Called by ushauri during the initialization of the environment

        :param config: ``pyramid.config`` object
        """


class IResource(Interface):
    """
        Allows to hook into the creation of JS and CSS libraries or resources
    """

    def add_libraries(self, config):
        """
        Called by ushauri so plugins can add new JS and CSS libraries to ushauri

        :param config: ``pyramid.config`` object
        :return Returns a dict array [{'name':'mylibrary','path':'/path/to/my/resources'}]
        """
        return []

    def add_JSResources(self, config):
        """
        Called by ushauri so plugins can add new JS Resources
        
        :param config: ``pyramid.config`` object        
        :return Returns a dict array [{'libraryname':'mylibrary','id':'myResourceID','file':'/relative/path/to/jsFile','depends':'resourceID'}]
        """
        return []

    def add_CSSResources(self, config):
        """
        Called by ushauri so plugins can add new CSS Resources

        :param config: ``pyramid.config`` object        
        :return Returns a dict array [{'libraryname':'mylibrary','id':'myResourceID','file':'/relative/path/to/jsFile','depends':'resourceID'}]
        """
        return []


class IPluralize(Interface):
    """
        Allows to hook into the pluralization function so plugins can extend the pluralization of ushauri
    """

    def pluralize(self, noun, locale):
        """
            Called the packages are created

            :param noun: ``Noun to be pluralized``
            :param locale: ``The current locate code e.g. en``
            :return the noun in plural form
        """


class ISchema(Interface):
    """
        Allows to hook into the schema layer and add new fields into it.
        The schema is a layer on top of the database schema so plugin developers can
        add new fields to ushauri tables without affecting the structure
        of the database. New fields are stored in extra as JSON keys
    """

    def update_schema(self, config):
        """
        Called by the host application so plugins can add new fields to table schemata

        :param config: ``pyramid.config`` object
        :return Returns a dict array [{'schema':'schema_to_update','fieldname':'myfield','fielddesc':'A good description of myfield'}]

        Plugin writers should use the utility functions:
            - addFieldToUserSchema
            - addFieldToProjectSchema
            - addFieldToEnumeratorSchema
            - addFieldToEnumeratorGroupSchema
            - addFieldToDataUserSchema
            - addFieldToDataGroupSchema
            - addFieldToFormSchema


        Instead of constructing the dict by themselves to ensure API compatibility

        """
        return []


class IDatabase(Interface):
    """
        Allows to hook into the database schema so plugins can add new tables
        After calling this
    """

    def update_schema(self, config, Base):
        """
        Called by the host application so plugins can add new tables to the database schema

        :param config: ``pyramid.config`` object
        :param Base: ``Sqlalchemy's declarative base`` object

        """


class IAuthorize(Interface):
    """
        Allows to hook into the user authorization
        After calling this
    """

    def after_login(self, request, user):
        """
        Called by the host application so plugins can modify the login of users

        :param request: ``pyramid.request`` object
        :param user: user object
        :return Return true or false if the login should continue. If False then a message should state why

        """
        return True, ""

    def before_register(self, request, registrant):
        """
        Called by the host application so plugins can do something before registering a user

        :param request: ``pyramid.request`` object
        :param registrant: Dictionary containing the details of the registrant
        :return Return true or false if the registrant should be added. If False then a message should state why

        """
        return True, ""

    def after_register(self, request, registrant):
        """
        Called by the host application so plugins do something after registering a user

        :param request: ``pyramid.request`` object
        :param registrant: Dictionary containing the details of the registrant

        """


class IPluginObserver(Interface):
    """
    Plugin to the plugin loading mechanism
    """

    def before_load(self, plugin):
        """
        Called before a plugin is loaded
        This method is passed the plugin class.
        """

    def after_load(self, service):
        """
        Called after a plugin has been loaded.
        This method is passed the instantiated service object.
        """

    def before_unload(self, plugin):
        """
        Called before a plugin is loaded
        This method is passed the plugin class.
        """

    def after_unload(self, service):
        """
        Called after a plugin has been unloaded.
        This method is passed the instantiated service object.
        """
