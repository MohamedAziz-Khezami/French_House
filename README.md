
# 🇫🇷 French House

This project focuses on analyzing and predicting house prices across France using key features such as location, surface area, number of rooms, and type of house.
To achieve high accuracy, we utilized a LightGBM Regressor, trained on an extensive dataset of 11 million records. This ensures precise and reliable predictions, making the model highly effective for real-world applications.



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

![Screenshot from 2024-12-11 08-58-15](https://github.com/user-attachments/assets/f24440f3-944b-4b69-8474-56b06baf3a18)

![Screenshot from 2024-12-11 08-51-34](https://github.com/user-attachments/assets/c73fc503-16c0-4d0e-a3d9-d4fca0d57183)

![Screenshot from 2024-12-11 08-49-21](https://github.com/user-attachments/assets/3d45fd24-d258-4e32-9df6-447b26e40fb1)

![Screenshot from 2024-12-11 08-49-45](https://github.com/user-attachments/assets/d80ed00c-e173-411b-8f9b-4db56fe8a1f2)

![Screenshot from 2024-12-11 08-49-58](https://github.com/user-attachments/assets/7c25f84c-4002-46a4-93fa-c619080c34f0)

![Screenshot from 2024-12-11 08-50-09](https://github.com/user-attachments/assets/efc1c175-cb53-43ff-bc77-dba658b411c8)





## Feedback

If you have any feedback, please reach out to us at mohamedazizkhezami@gmail.com
