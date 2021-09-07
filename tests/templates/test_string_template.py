import pytest
from tests.utils import PASS, FAIL

from litemake.parse.endpoints import StringTemplate
from litemake.exceptions import litemakeTemplateError


class TestStringTemplates:

    def _test_string_arg(self, value, expected, **build):
        t = StringTemplate(**build)

        if expected == PASS:
            t.validate(value, fieldpath=list())

        else:
            with pytest.raises(litemakeTemplateError):
                t.validate(value, fieldpath=list())

    @pytest.mark.parametrize('value, expected', [
        ('hello', PASS),
        ('', PASS),
        (' ', PASS),
        ('0', PASS),
        (0, FAIL),
        (None, FAIL),
        (False, FAIL),
        (True, FAIL),
    ])
    def test_no_kwargs(self, value, expected):
        self._test_string_arg(value, expected)

    @pytest.mark.parametrize('value, expected', [
        ('long long string', PASS),
        ('lo', PASS),
        ('1', PASS),
        ('', FAIL),
    ])
    def test_min_one(self, value, expected):
        self._test_string_arg(value, expected, min_len=1)

    @pytest.mark.parametrize('value, expected', [
        ('', PASS),
        ('0', PASS),
        ('None', PASS),
    ])
    def test_min_zero(self, value, expected):
        self._test_string_arg(value, expected, min_len=0)

    @pytest.mark.parametrize('value, expected', [
        ('0', FAIL),
        ('5', FAIL),
        ('12345', PASS),
        ('hello there', PASS),
    ])
    def test_min_five(self, value, expected):
        self._test_string_arg(value, expected, min_len=5)

    @pytest.mark.parametrize('value, expected', [
        ('', PASS),
        ('o', PASS),
        ('ש', PASS),
        ('🗼', PASS),
    ])
    def test_max_one(self, value, expected):
        self._test_string_arg(value, expected, max_len=1)

    @pytest.mark.parametrize('value, expected', [
        ('', PASS),
        (' ', FAIL),
        ('\n', FAIL),
    ])
    def test_max_zero(self, value, expected):
        self._test_string_arg(value, expected, max_len=0)

    @pytest.mark.parametrize('value, expected', [
        ('1', PASS),
        ('', PASS),
        ('HELLO', PASS),
        ('HELLO!', FAIL),
    ])
    def test_max_five(self, value, expected):
        self._test_string_arg(value, expected, max_len=5)

    @pytest.mark.parametrize('allowed, value, expected', [
        ('abc', 'aaabbbbbbcccccc', PASS),
        ('abc', 'abc abc', FAIL),
        ('', '', PASS),
        ('', ' ', FAIL),
        (' ', '    ', PASS),
        (' ', '\t', FAIL),
    ])
    def test_allowed_chars(self, allowed, value, expected):
        self._test_string_arg(value, expected, allowed_chars=allowed)

    @pytest.mark.parametrize('banned, value, expected', [
        ('a', 'Hello there!', PASS),
        ('l', 'Hello there!', FAIL),
        ('er', 'Hello there!', FAIL),
    ])
    def test_no_repeating(self, banned, value, expected):
        self._test_string_arg(value, expected, no_repeating=banned)

    @pytest.mark.parametrize('banned, value, expected', [
        ('a', 'Hello there!', PASS),
        ('e', 'Hello there!', PASS),
        ('!', 'Hello there!', FAIL),
        ('H', 'Hello there!', FAIL),
        ('H!', 'Hello there!', FAIL),
    ])
    def test_no_on_edges(self, banned, value, expected):
        self._test_string_arg(value, expected, no_on_edges=banned)
