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
