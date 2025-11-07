"""
Day 7: Accessibility - Read Canal GeoJson, do some calculations, and plot.

Canals: https://data-canalrivertrust.opendata.arcgis.com/datasets/f3c249d59f0b464d8b09d25e39305a99_4/explore
Cities: https://simplemaps.com/data/gb-cities
"""

import csv
import json

import matplotlib.pyplot as plt
from cartopy import crs as ccrs
from cartopy import feature as cfeature
from pyproj import Transformer
from shapely.geometry import LineString, MultiLineString, shape


def project_line(shape, transformer):
    """Project a line to another system."""
    x, y = shape.coords.xy
    x_proj, y_proj = transformer.transform(x, y)
    return LineString(zip(x_proj, y_proj, strict=True))


# Define transformer (WGS84 to British National Grid)
my_transformer = Transformer.from_crs("epsg:4326", "epsg:27700", always_xy=True)

with open("Canals_by_Navigation_(Lines)_3119668797985249099.geojson", "r") as file:
    canal_geojson = json.load(file)

canal_dict_ll = {}
for i, feature in enumerate(canal_geojson["features"]):
    props = feature.get("properties", {})
    geom_type = feature["geometry"]["type"]
    print(f"Feature {i}:")
    print(f"  Geometry type: {geom_type}")
    print(f"  Properties: {props}")

    # Place in a dict of countries
    canal_dict_ll[props.get("sapcanalcode")] = shape(feature)


canal_dict_km = {}
for name, canal in canal_dict_ll.items():
    if canal.geom_type == "MultiLineString":
        canal_dict_km[name] = MultiLineString(
            [project_line(p, my_transformer) for p in canal.geoms]
        )
    else:
        canal_dict_km[name] = project_line(canal, my_transformer)

for name, canal in canal_dict_km.items():
    print(f"Country: {name}")
    print(f"Type: {canal.geom_type}")
    print(f"Length [km]: {canal.length / 1000:.2f}")

cities = {}
with open("cities.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        name = row[0]
        lat = float(row[1])
        lon = float(row[2])
        cities[name] = (lon, lat)  # (lon, lat) tuple

# Plot using cartopy on a UK map
projection = ccrs.Mercator(central_longitude=0)
transform = ccrs.PlateCarree()

fig2 = plt.figure(figsize=(6, 8), constrained_layout=True)
ax2 = plt.subplot(1, 1, 1, projection=projection)
ax2.set_extent([-10, 2.5, 50, 60])
ax2.coastlines()

for _name, coords in cities.items():
    ax2.plot(coords[0], coords[1], "ko", transform=transform)

for _name, canal in canal_dict_ll.items():
    if canal.geom_type == "MultiLineString":
        for item in canal.geoms:
            x, y = item.coords.xy
            ax2.plot(x, y, "b-", transform=transform)
    else:
        x, y = canal.coords.xy
        ax2.plot(x, y, "b-", transform=transform)

ax2.set_xlabel("lon")
ax2.set_ylabel("lat")
ax2.set_title("UK Canals and cities over 200,000 population.")
gl = ax2.gridlines(
    draw_labels=True, linewidth=1, color="gray", alpha=0.5, linestyle="--"
)

plt.savefig("UK_canals.svg")
plt.close()
