"""Day 3: Polygons - Read ONS GeoJson, do some calculations, and plot."""

import json

import matplotlib.pyplot as plt
from cartopy import crs as ccrs
from cartopy import feature as cfeature
from pyproj import Transformer
from shapely.geometry import MultiPolygon, Polygon, shape


def project_polygon(polygon, transformer):
    """Project a polygon to another system."""
    x, y = polygon.exterior.xy
    x_proj, y_proj = transformer.transform(x, y)
    return Polygon(zip(x_proj, y_proj, strict=True))


with open("UK-countries.json", "r") as file:
    uk_geojson = json.load(file)

# Define transformer (WGS84 to British National Grid)
my_transformer = Transformer.from_crs("epsg:4326", "epsg:27700", always_xy=True)


country_dict_ll = {}
for i, feature in enumerate(uk_geojson["features"]):
    props = feature.get("properties", {})
    geom_type = feature["geometry"]["type"]
    print(f"Feature {i}:")
    print(f"  Geometry type: {geom_type}")
    print(f"  Properties: {props}")

    # Place in a dict of countries
    country_dict_ll[props.get("CTRY24NM")] = shape(feature)

country_dict_km = {}
for name, country in country_dict_ll.items():
    # Handle MultiPolygon and Polygon
    if country.geom_type == "MultiPolygon":
        country_dict_km[name] = MultiPolygon(
            [project_polygon(p, my_transformer) for p in country.geoms]
        )
    else:
        country_dict_km[name] = project_polygon(country, my_transformer)

for name, country in country_dict_km.items():
    print(f"Country: {name}")
    print(f"Type: {country.geom_type}")
    print(f"Area [km2]: {country.area / 1000**2:.2f}")
    print(f"Area [deg]: {country_dict_ll[name].area}")
    print(f"Bounds: {country.bounds}")
    print(f"Length (perimeter) [km]: {country.length / 1000}")
    if country.geom_type == "MultiPolygon":
        num_exterior_points = sum(len(p.exterior.coords) for p in country.geoms)
        print(f"Number of exterior points (total): {num_exterior_points}")
    else:
        print(f"Number of exterior points: {len(country.exterior.coords)}")

# Plot using cartopy on a UK map
projection = ccrs.Mercator(central_longitude=0)
transform = ccrs.PlateCarree()

fig2 = plt.figure(figsize=(6, 8), constrained_layout=True)
ax2 = plt.subplot(1, 1, 1, projection=projection)
ax2.set_extent([-15, 5, 48, 62])
ax2.coastlines()

color_map = {
    "Wales": "red",
    "Northern Ireland": "green",
    "Scotland": "blue",
    "England": "grey",
}

for name, country in country_dict_ll.items():
    ax2.add_geometries(
        [country],
        crs=transform,
        edgecolor="red",
        facecolor=color_map.get(name, "none"),
        linewidth=0.5,
    )
    centroid = country.centroid
    ax2.plot(centroid.x, centroid.y, "ro", transform=transform)
    area_km2 = country_dict_km[name].area / 1e6
    ax2.text(
        centroid.x,
        centroid.y+1,
        f"{name}\n{area_km2:.1f} km2",
        transform=transform,
        fontsize=8,
        ha="center",
        va="bottom",
        bbox={"facecolor": "white", "alpha": 0.75, "edgecolor":"none"},
    )

ax2.set_xlabel("lon")
ax2.set_ylabel("lat")
ax2.set_title("UK Country Areas")
gl = ax2.gridlines(
    draw_labels=True, linewidth=1, color="gray", alpha=0.5, linestyle="--"
)

plt.savefig("UK_map.png", dpi=300)
plt.close()
