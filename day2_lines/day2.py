"""Day 1: Points - Read Cambridge location from GeoJson to shapely vector and plot."""

import json

import antimeridian
import matplotlib.pyplot as plt
from cartopy import crs as ccrs
from shapely.geometry import LineString, Polygon, shape

# GeoJson is a way to represent vector data in a Json format
# Read in a point representing Cambridge from file
with open("verne.json", "r") as file:
    verne_geojson = json.load(file)

# Convert to a vector points representation using shapely
verne_points = shape(verne_geojson)
print(f"Multipoint Object from file:\n{verne_points}")

verne_line = LineString(verne_points.geoms)
print(f"Line from Multipoints:\n{verne_line}")

# verne_lineFix antimeridian crossings
verne_line = antimeridian.fix_line_string(verne_line, great_circle=False)
print(f"Line after antimeridian fix:\n{verne_line}")

verne_polygon = Polygon(verne_line.geoms[0].coords)
print(f"Polygon from LineString:\n{verne_polygon}")

# Plot using cartopy
# Cartopy provides a stock image background, but needs scipy to transform
projection = ccrs.Robinson(central_longitude=0)
transform = ccrs.PlateCarree()

fig2 = plt.figure(figsize=(12, 8), constrained_layout=True)
ax2 = plt.subplot(1, 1, 1, projection=projection)
ax2.coastlines()
ax2.stock_img()

for line in verne_line.geoms:
    verne_x, verne_y = line.xy
    ax2.plot(verne_x, verne_y, "r--", lw=2, transform=transform)

ax2.set_global()

gl = ax2.gridlines(
    draw_labels=True, linewidth=1, color="gray", alpha=0.5, linestyle="--"
)

ax2.set_xlabel("lon")
ax2.set_ylabel("lat")
ax2.set_title("Le Tour du monde en 80 jours", fontsize=16)

plt.savefig("80-days.svg")
plt.close()
