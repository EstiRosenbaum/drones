from server.config import Config
from server.map import Map

config = Config(
    "/Users/doronsemama/PycharmProjects/routes/server/artifacts/israel.tif",
    "/Users/doronsemama/PycharmProjects/routes/server/artifacts/birds_shit.kml",
    "/Users/doronsemama/PycharmProjects/routes/server/artifacts/birds_shit.kml",
)
config.set_safety_angle_from_peak_los(100)
config.set_location_error_radius(1000)
config.set_min_distance_from_surface_height(300)

geo_map = Map(config).init()
xb = (441494, 899999)
yb = (3140757, 3845296)

focused_map = geo_map.focus(xb, yb)

focused_map.save(
    "/Users/doronsemama/PycharmProjects/routes/server/artifacts/israel.tif"
)
