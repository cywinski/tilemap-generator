from tilemap import TileMap

tilemap1 = TileMap(20, 30, [], {}, 10, 20)
tilemap2 = TileMap(20, 30, ['water', 'land', 'sand'], {'black': (0, 0, 0)})
tilemap3 = TileMap(10, 10, [], {}, 4)


def test_colors_to_use():
    assert tilemap1.colors_to_use() == [(51, 153, 255), (125, 200, 100)]
    assert tilemap2.colors_to_use() == [(51, 153, 255), (125, 200, 100),
                                        (255, 255, 153), (0, 0, 0)]


def test_central_pts_to_array():
    ls_of_rows = [j for i in tilemap1.central_pts_to_array(
        tilemap1.zeros_array.tolist(),
        TileMap.amount_central_pts
        (
         tilemap1.width,
         tilemap1.height,
         tilemap1.grounds,
         tilemap1.own_grounds,
         tilemap1.min_pts,
         tilemap1.max_pts
        )
    ) for j in i]
    assert ((51, 153, 255) in ls_of_rows) is True
    assert ((125, 200, 100) in ls_of_rows) is True


def test_amount_central_pts():
    assert tilemap1.amount_central_pts(
        tilemap1.width,
        tilemap1.height,
        tilemap1.grounds,
        tilemap1.own_grounds,
        tilemap1.min_pts,
        tilemap1.max_pts
    ) >= 10
    assert tilemap1.amount_central_pts(
        tilemap1.width,
        tilemap1.height,
        tilemap1.grounds,
        tilemap1.own_grounds,
        tilemap1.min_pts,
        tilemap1.max_pts
    ) <= 20
    assert tilemap2.amount_central_pts(
        tilemap2.width,
        tilemap2.height,
        tilemap2.grounds,
        tilemap2.own_grounds,
        tilemap2.min_pts,
        tilemap2.max_pts
    ) >= 10
    assert tilemap2.amount_central_pts(
        tilemap2.width,
        tilemap2.height,
        tilemap2.grounds,
        tilemap2.own_grounds,
        tilemap2.min_pts,
        tilemap2.max_pts
    ) <= 15
    assert tilemap3.amount_central_pts(
        tilemap3.width,
        tilemap3.height,
        tilemap3.grounds,
        tilemap3.own_grounds,
        tilemap3.min_pts,
        tilemap3.max_pts
    ) >= 4


def test_measure_distances():
    ls_of_rows = [j for i in tilemap1.measure_distances(
                  tilemap1.list_central_pts)
                  for j in i]
    assert (0 in ls_of_rows) is False


def test_expand_image():
    assert tilemap1.expand_image().size == (tilemap1.width*16, tilemap1.height*16)
