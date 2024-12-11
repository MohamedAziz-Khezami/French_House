
# 🇫🇷 French House
---
This project aims to study and predict the prices of houses in France based on the location, Surface, number of rooms, and type of the house.
The regression model which is a LightGBM regressor, was trained on a 11 Million rows of data to deliver the most precise predictions.

---

## Used Libraries

The main libraries used in this project:

- `dash`: an open-source framework for building data visualization interfaces. Released in 2017 as a Python library
- `pandas`: a fast, powerful, flexible and easy to use open source data analysis and manipulation tool.
- `geopandas`: an open source project to make working with geospatial data in python easier.
- `numpy`: a Python library adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays.
- `plotly`: an open-source module of Python that is used for data visualization and supports various graphs like line charts, scatter plots, bar charts, histograms, area plots, etc.
- `LightGBM`: an open-source tool enabling highly efficient training over large scale datasets with low memory cost. LightGBM adopts two novel techniques Gradient-based One-Side Sampling (GOSS) and Exclusive Feature Bundling (EFB).
- `Verstack`: A library that offers a variety of tools like NANImputers, and a hyperparameter optimizer for lightGBM.
- `requests`: allows you to send HTTP requests using Python. The HTTP request returns a Response Object with all the response data.



## API Reference

The API used for identifying the location of addresses is `mapbox Geocoding API`.



```python
def get_coordinates_with_requests(address):
    """Get longitude and latitude for a given address using requests."""
    base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places"
    # Construct the API URL
    url = f"{base_url}/{address}.json"
    params = {
        "access_token": mapbox_access_token,
        "limit": 1,  # Get only the most relevant result
    }
    # Make the API request
    response = requests.get(url, params=params)
```

## Installation

In your terminal 

```python
$ git clone https://github.com/MohamedAziz-Khezami/French_House.git
$ cd French_House
```

Then go to `/src/app.py` and run the program manually or 

```pyton
$ python /src/app.py
```

Then go to `http://127.0.0.1:8050/`. You should be able to see the app running.

## Screenshots










## Feedback

If you have any feedback, please reach out to us at mohamedazizkhezami@gmail.com