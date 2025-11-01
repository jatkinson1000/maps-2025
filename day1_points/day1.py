"""Day 1: Points - Read Cambridge location from GeoJson to shapely vector and plot."""

import json

import matplotlib.pyplot as plt
from cartopy import crs as ccrs
from cartopy import feature as cfeature
from shapely.geometry import Point, shape

plt.rcParams.update({"font.size": 12})

# GeoJson is a way to represent vector data in a Json format
# Read in a point representing Cambridge from file
with open("GJ-point.json", "r") as file:
    cbg_geojson = json.load(file)
print(f"Json read from file: {cbg_geojson}")

# Convert to a vector pont representation using shapely
# Note that the point is (x, y) -> (lon, lat)
cbg_json_point = shape(cbg_geojson)
print(f"Converted to shapely vector point: {cbg_json_point}")

# Compare to manual definition of point using shapely
cbg_manual_point = Point(0.1181, 52.2054)
print(f"Manual definition of vector point: {cbg_manual_point}")

# Plot basic point
fig1, ax1 = plt.subplots(figsize=(6, 8), constrained_layout=True)
ax1.plot(cbg_json_point.x, cbg_json_point.y, "ro")
ax1.set_xlabel("lon")
ax1.set_ylabel("lat")
ax1.set_title("Cambridge UK")

plt.savefig("cambridge_basic.svg")
plt.close()

# Plot using cartopy on a UK map
# Cartopy provides a CRS module
# Note projection is not the same as transformation!
# For transformations use PlateCaree
projection = ccrs.Mercator(central_longitude=0)
transform = ccrs.PlateCarree()

fig2 = plt.figure(figsize=(6, 8), constrained_layout=True)
ax2 = plt.subplot(1, 1, 1, projection=projection)
ax2.set_extent([-15, 5, 48, 62])
ax2.coastlines()
ax2.plot(cbg_json_point.x, cbg_json_point.y, "ro", transform=transform)
ax2.set_xlabel("lon")
ax2.set_ylabel("lat")
ax2.set_title("Cambridge UK")
gl = ax2.gridlines(
    draw_labels=True, linewidth=1, color="gray", alpha=0.5, linestyle="--"
)

plt.savefig("cambridge_map.svg")
plt.close()
