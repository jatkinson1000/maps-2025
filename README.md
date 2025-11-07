# 30 Day Map Challenge 2025

GIS is a skill gap I've been wanting to fill for a while.
On a whim I've decided to do the [30 Day Map Challenge](https://30daymapchallenge.com/).

To learn I'm going to be reading
[Python for Geographic Data Analysis](https://pythongis.org/).

Resources:

- The [GeoJson Specification](https://geojson.org/)
- [Project Pythia](https://foundations.projectpythia.org/)

Below are details of the what I have done and learnt.

- Day 1: Points\
  Created a GeoJson file with the coordinates of Cambridge.
  Read in using `shapely` and plotted using `cartopy`.
    - Cartopy projection and transform are
      [not the same](https://cartopy.readthedocs.io/stable/tutorials/understanding_transform.html)
    - Points are `(x, y) -> (lon, lat)`
- Day 2: Lines\
  Plotted the (crow's) route from Jules Verne's round the world in 80 days.
  Read in as MultiPoint and converted using `shapely`, and plotted using `cartopy`.
    - Antimeridian splitting is a challenge - used the
      [antimeridian](https://github.com/gadomski/antimeridian) package.
    - Played with a projection options for too long and cartopy now makes it   easy to add a stock image.
- Day 3: Polygons\
  Obtained [real data of UK borders](https://geoportal.statistics.gov.uk/datasets/ons::countries-december-2024-boundaries-uk-bfc-2/about),
  converted to km, obtained some data using shapely and plotted.
    - Decided to try and get some real data from [UK ONS](https://geoportal.statistics.gov.uk/) - UK country boundaries.
    - Used Shapely to get perimeter, area, and centroid.
    - Had to use Proj (OMG, real GIS!!) to convert from lat-lon to km based on
      [EPSG Parameters Sets](https://en.wikipedia.org/wiki/EPSG_Geodetic_Parameter_Dataset)
      see also [spatialreference.org](https://spatialreference.org/)
- Day 7: Accessibility\
  Obtained [UK canals in GeoJSON](https://data-canalrivertrust.opendata.arcgis.com/datasets/f3c249d59f0b464d8b09d25e39305a99_4/explore)
  and plotted along with [cities over 200,000](https://simplemaps.com/data/gb-cities).
    - A long-held belief of mine is that canals in the UK are greatly
      under-utilised and we should move more this way instead of by road.
      Plotting shows this is perhaps due to growing up in the Midlands
      where they are most prevalent. Scotland or the South are largely
      inaccessible via canal. Historically this makes sense as we see
      connections run between industrial centres with a stretch down to
      London.
    - Used Shapely to estimate the longest canal to be the Grand Union
      at 210.7km (wikipedia says 220km).

Notes for later:

- [elevatr](https://github.com/titouanlegourrierec/elevatr) for terrain maps?


## Usage

Requirements are in `requirements.txt` and can be installed with pip.

Exercises are a single directory per day and save a single image to file.
The main file to be run for each day is `day<n>.py`


## License
Copyright &copy; Jack Atkinson

The code in this repo is distributed under the
[GPL-3.0 Licence](https://github.com/jatkinson1000/maps-2025/blob/main/LICENSE).


## Contributing

This repo is intended as a place to log and store my progress in the challenge.
I do not expect it to attract or require contributions.
If, for some reason, you want to feed back on the code please open an issue.
