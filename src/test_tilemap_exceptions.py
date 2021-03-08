import pytest
from tilemap_exceptions import (
    InvalidData,
    verify_dimensions,
    verify_pts,
    verify_grounds
    )


def test_verify_dimensions():
    with pytest.raises(InvalidData):
        verify_dimensions('', 10)
        verify_dimensions('abc', 10)
        verify_dimensions(-2, 5)
        verify_dimensions(2, 2, ['water', 'land', 'forest', 'stone', 'sand'])
        verify_dimensions(2, 2, ['water', 'land', 'forest', 'stone'],
                          {'black': (0, 0, 0)})
        verify_dimensions(2, 2, [], {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'green': (0, 255, 0),
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            })


def test_verify_pts():
    with pytest.raises(InvalidData):
        verify_pts(10, 10, min_pts='a')
        verify_pts(5, 5, min_pts=10)
        verify_pts(5, 5, min_pts=1)
        verify_pts(10, 10, max_pts='a')
        verify_pts(5, 5, max_pts=1)
        verify_pts(5, 5, min_pts=10, max_pts=3)


def test_verify_grounds():
    with pytest.raises(InvalidData):
        verify_grounds(2, 2, ['water', 'land', 'forest', 'stone', 'sand'])
        verify_grounds(10, 10, ['ocean'])
        verify_grounds(10, 10, own_grounds=(0, 0, 0))
        verify_grounds(10, 10, own_grounds={'black': [0, 0, 0]})
        verify_grounds(10, 10, own_grounds={'black': (0, 0)})
        verify_grounds(10, 10, own_grounds={'black': (-1, 0, 300)})
