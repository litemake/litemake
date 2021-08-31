import pytest
from nanomake.parse.templates import SetupStringArg

PASS = True
FAIL = False


class TestStringTemplates:

    def _test_string_arg(self, value, expected, **build):
        t = SetupStringArg(**build)

        if expected == PASS:
            t.validate(value)

        else:
            with pytest.raises(AssertionError):
                t.validate(value)

    @pytest.mark.parametrize('value, expected', [
        (123, FAIL),
        (9_999_999, FAIL),
        ('long long string', PASS),
        ('lo', PASS),
        ('1', PASS),
        ('', FAIL),
    ])
    def test_min_one(self, value, expected):
        self._test_string_arg(value, expected, min_len=1)

    @pytest.mark.parametrize('value, expected', [
        (123, FAIL),
        (0, FAIL),
        ('', PASS),
        ('0', PASS),
        ('None', PASS),
    ])
    def test_min_zero(self, value, expected):
        self._test_string_arg(value, expected, min_len=0)

    @pytest.mark.parametrize('value, expected', [
        (12345, FAIL),
        (True, FAIL),
        ('0', FAIL),
        ('5', FAIL),
        ('12345', PASS),
        ('hello there', PASS),
    ])
    def test_min_five(self, value, expected):
        self._test_string_arg(value, expected, min_len=5)

    @pytest.mark.parametrize('value, expected', [
        (1234, FAIL),
        (0, FAIL),
        (None, FAIL),
        (True, FAIL),
        (False, FAIL),
        ('', PASS),
        ('o', PASS),
        ('ש', PASS),
        ('🗼', PASS),
    ])
    def test_max_one(self, value, expected):
        self._test_string_arg(value, expected, max_len=1)

    @pytest.mark.parametrize('value, expected', [
        (0, FAIL),
        ('', PASS),
        (' ', FAIL),
        ('\n', FAIL),
        (123, FAIL),
        (False, FAIL),
        (None, FAIL),
    ])
    def test_max_zero(self, value, expected):
        self._test_string_arg(value, expected, max_len=0)

    @pytest.mark.parametrize('value, expected', [
        (12, FAIL),
        (1234567, FAIL),
        ('1', PASS),
        ('', PASS),
        ('HELLO', PASS),
        ('HELLO!', FAIL),
    ])
    def test_max_five(self, value, expected):
        self._test_string_arg(value, expected, max_len=5)
