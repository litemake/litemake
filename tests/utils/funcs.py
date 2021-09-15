def matching_msg(expected: str, got: str) -> bool:
    """ Checks if the 'got' string contains the 'expected' string. Returns
    True only if the 'got' string is contained inside the 'expected' string. """
    expected, got = expected.lower(), got.lower()
    return expected in got
