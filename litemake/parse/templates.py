import typing
from abc import ABC, abstractmethod
from copy import deepcopy

from litemake.exceptions import litemakeTemplateError


class MISSING:
    """ A dummy object that replaces `None` where `None` is a valid value, but
    we want to distinguish between the user explicitly providing `None` and a
    default value. """


class BaseTemplate(ABC):

    @abstractmethod
    def validate(self, value, fieldpath: typing.List[str]):
        ''' An abstract method that will receive a value, and will validate it.
        The validation proccess can throw an error if the value is completely
        irrelevant, or change it and return the new value. '''

    @staticmethod
    def assert_type(value, type, fieldpath: typing.List[str]) -> None:
        ''' A helper method that receives a value and type, and raises an
        assertion error if the given value doesn't match the given type. '''

        if not isinstance(value, type):

            # Generate strings of class names
            required_name = type.__name__
            value_type_name = value.__class__.__name__

            # Construct error message
            required = f'Expected type {required_name!r}'
            notwhat = f'not {value_type_name!r} ({value!r})'

            # Assert type, throw message if assertion fails
            raise litemakeTemplateError(fieldpath, f'{required}, {notwhat}')


class Template(BaseTemplate):

    def __init__(self, **templates):
        self.templates: typing.Dict[str, BaseTemplate] = templates

    def validate(self, value, fieldpath: typing.List[str]) -> dict:

        if value is MISSING:
            # if the user didn't provide his own data, we will assume
            # that an empty dict is provided. This is implemented to allow
            # default values inside dictionaries to be applied.
            value = dict()

        self.assert_type(value, dict, fieldpath)

        keys = set(value.keys()).union(self.templates.keys())
        new = dict()
        for key in keys:
            field = fieldpath + [key]

            if key in self.templates:
                new[key] = self.templates[key].validate(
                    value.get(key, MISSING), field)

            else:
                raise litemakeTemplateError(field, 'Unexpected field')

        return new


class TemplateEndpoint(BaseTemplate):

    def __init__(self, default=MISSING):
        """ If default is not MISSING, the endpoint isn't required. """
        self.required = default is MISSING
        self.default = default

    def validate(self, value, fieldpath: typing.List[str]):
        """ Validates that the given value is provided if required by the
        template, and if not provided -> raises an exception.
        If the value isn't provided but also isn't required, return the
        default value that is provided by the template. Otherwise, returns
        the given value. """

        if self.required and value is MISSING:
            raise litemakeTemplateError(fieldpath, 'Missing required field')

        elif not self.required and value is MISSING:
            return deepcopy(self.default)

        else:
            return value
