# 3. Comprehensive Data Ingestion Pipeline & Feature Engineering

## Overview

The predictive capability of PyroCast relies on the continuous ingestion of heterogeneous geospatial datasets from multiple authoritative sources. These datasets collectively describe the **current wildfire state**, **terrain morphology**, **vegetation fuel characteristics**, and **meteorological conditions**, enabling the AI model to simulate wildfire propagation under dynamically changing environmental conditions.

Each prediction request begins by defining a **Bounding Box (BBOX)** representing the geographical Area of Interest (AOI).

```
Bounding Box Format

min_longitude,min_latitude,max_longitude,max_latitude

Example

-119.65,37.70,-119.50,37.85
```

All incoming datasets are reprojected into the **WGS84 Coordinate Reference System (EPSG:4326)** before spatial alignment.

---

# 3.1 Data Sources

The system integrates four major categories of data:

| Category              | Provider      | Purpose                                       |
| --------------------- | ------------- | --------------------------------------------- |
| Active Fire Detection | NASA FIRMS    | Detect current wildfire ignition points       |
| Terrain & Fuel        | USGS LANDFIRE | Understand topography and burnable vegetation |
| Weather Forecast      | NOAA HRRR     | Predict atmospheric influence on fire spread  |
| Historical Fire Data  | MTBS / NIFC   | Model training and validation                 |

---

# 3.2 NASA FIRMS — Active Fire Detection

## Purpose

NASA FIRMS provides near real-time satellite observations of thermal anomalies detected by MODIS and VIIRS satellites.

These detections represent the current ignition points of active wildfires and serve as the initial condition for wildfire propagation prediction.

Instead of manually reporting fire locations, the platform automatically retrieves newly detected hotspots every time a simulation begins.

---

## Data Characteristics

**Provider**

NASA FIRMS

**Satellite Missions**

* MODIS
* VIIRS

**Refresh Frequency**

* MODIS: Every ~12 hours
* VIIRS: Approximately every 6 hours

**API**

```
https://firms.modaps.eosdis.nasa.gov/api/area/csv/
```

Authentication is performed using the registered NASA FIRMS API Key stored securely in the environment configuration.

---

## Retrieved Attributes

| Field                  | Description                |
| ---------------------- | -------------------------- |
| Latitude               | Fire pixel latitude        |
| Longitude              | Fire pixel longitude       |
| Brightness Temperature | Thermal intensity (Kelvin) |
| Acquisition Date       | Date of observation        |
| Acquisition Time       | UTC timestamp              |
| Confidence             | Detection confidence       |
| FRP                    | Fire Radiative Power       |
| Satellite              | MODIS or VIIRS             |

---

## Why It Matters

The active fire pixels become the initial ignition mask used by the neural network.

Without this dataset, the system would have no knowledge of where the wildfire currently exists.

---

# 3.3 LANDFIRE — Terrain & Fuel Characteristics

Wildfire behavior is heavily constrained by terrain and vegetation.

LANDFIRE provides high-resolution raster datasets describing the physical landscape over which the wildfire propagates.

Resolution:

30 meters

---

## Retrieved Layers

### Elevation

Digital Elevation Model (DEM)

Used to compute:

* Slope
* Aspect
* Terrain Gradient

---

### Slope

Derived from DEM.

Fire naturally spreads faster uphill because radiant heat preheats vegetation located above the flame front.

---

### Aspect

Represents the compass direction of slopes.

South-facing slopes receive more solar radiation, reducing fuel moisture and increasing ignition probability.

---

### Vegetation Type

Classifies vegetation into standardized fuel categories.

Examples include:

* Grasslands
* Shrublands
* Mixed Forest
* Dense Conifer
* Chaparral

Each vegetation type exhibits different combustion behavior.

---

### Fuel Loading

Represents combustible biomass available per unit area.

Higher fuel loads increase flame intensity and fire duration.

---

### Canopy Density

Indicates tree coverage.

Dense canopies increase crown fire probability.

---

# Why Terrain Matters

Terrain influences wildfire propagation through:

* Convective heating
* Wind channeling
* Fuel continuity
* Natural barriers
* Elevation gradients

The terrain layer provides the physical constraints under which the wildfire evolves.

---

# 3.4 NOAA HRRR Weather Forecast

Weather is the single largest dynamic driver of wildfire spread.

The High Resolution Rapid Refresh (HRRR) model provides hourly atmospheric forecasts at approximately 3 km resolution.

These forecasts are updated continuously and allow PyroCast to predict how the fire will evolve over the coming hours rather than simply describing its current state.

---

## Retrieved Variables

### Wind Speed

Controls flame tilt and ember transport.

Higher wind speeds increase the Rate of Spread (ROS).

---

### Wind Direction

Determines the primary propagation vector.

The predicted burn perimeter elongates along the prevailing wind direction.

---

### Relative Humidity

Acts as a proxy for vegetation moisture.

Lower humidity increases ignition probability.

---

### Air Temperature

Higher temperatures reduce fuel moisture content.

---

### Surface Pressure

Influences regional atmospheric circulation.

---

### Precipitation

Rainfall suppresses combustion.

The model significantly reduces burn probability after measurable precipitation.

---

### Soil Moisture (Optional)

Provides an estimate of subsurface fuel moisture.

---

## Weather Variables Used

| Variable          | Symbol | Unit   |
| ----------------- | ------ | ------ |
| Wind U Component  | UGRD   | m/s    |
| Wind V Component  | VGRD   | m/s    |
| Relative Humidity | RH     | %      |
| Air Temperature   | TMP    | Kelvin |
| Surface Pressure  | PRES   | Pa     |
| Precipitation     | APCP   | mm     |

---

# 3.5 Historical Fire Dataset

Historical wildfire perimeters are required for supervised training.

Possible sources include:

* MTBS
* National Interagency Fire Center
* CAL FIRE
* Global Wildfire Information System

Historical datasets provide:

* Fire perimeter evolution
* Burn duration
* Final burned area
* Fuel consumption

These labels enable the neural network to learn realistic wildfire behavior.

---

# 3.6 Unified Feature Tensor

After ingestion, every dataset is transformed into a common spatial grid.

The aligned tensor has dimensions:

```
Channels × Height × Width
```

Example

```
14 × 512 × 512
```

Each channel represents one environmental variable.

| Channel | Feature              |
| ------- | -------------------- |
| 1       | Active Fire Mask     |
| 2       | Fire Radiative Power |
| 3       | Elevation            |
| 4       | Slope                |
| 5       | Aspect               |
| 6       | Vegetation Type      |
| 7       | Fuel Load            |
| 8       | Canopy Density       |
| 9       | Wind U               |
| 10      | Wind V               |
| 11      | Relative Humidity    |
| 12      | Temperature          |
| 13      | Surface Pressure     |
| 14      | Precipitation        |

This tensor becomes the direct input to the Physics-Informed Neural Network.

---

# 3.7 Physics-Based Fire Behaviour Modeling

Unlike traditional deep learning models, PyroCast incorporates established wildfire propagation physics into the optimization process. These physical constraints ensure that predictions remain scientifically plausible while still allowing the neural network to learn complex nonlinear relationships from historical wildfire events.

## Physical Variables Considered

| Variable                   | Influence on Fire Spread                             |
| -------------------------- | ---------------------------------------------------- |
| Wind Speed                 | Accelerates flame front and transports embers        |
| Wind Direction             | Determines dominant spread direction                 |
| Terrain Slope              | Increases uphill spread due to convective preheating |
| Aspect                     | Influences solar exposure and fuel dryness           |
| Fuel Load                  | Controls combustion intensity and duration           |
| Vegetation Type            | Determines burn rate and flame characteristics       |
| Air Temperature            | Reduces fuel moisture, increasing ignition potential |
| Relative Humidity          | Higher humidity suppresses ignition and spread       |
| Precipitation              | Dampens fuels and lowers burn probability            |
| Fire Radiative Power (FRP) | Estimates current fire intensity                     |

## Core Fire Behaviour Equations

### 1. Rothermel Surface Fire Spread Model

Used to estimate the **Rate of Spread (ROS)** based on fuel characteristics, wind, and slope.

[
R = \frac{I_R \times \xi \times (1 + \phi_w + \phi_s)}
{\rho_b \times \epsilon \times Q_{ig}}
]

Where:

* (R): Rate of Spread (m/min)
* (I_R): Reaction intensity
* (\phi_w): Wind factor
* (\phi_s): Slope factor
* (\rho_b): Bulk fuel density
* (\epsilon): Effective heating number
* (Q_{ig}): Heat of pre-ignition

### 2. Wind Vector Calculation

The horizontal wind field is reconstructed from the HRRR U and V components:

[
V = \sqrt{U^2 + V^2}
]

[
\theta = \tan^{-1}\left(\frac{V}{U}\right)
]

where:

* (V): Wind speed
* (\theta): Wind direction

These vectors directly influence the predicted fire propagation direction.

### 3. Terrain Slope

Slope is derived from the Digital Elevation Model (DEM):

[
Slope = \tan^{-1}\left(\sqrt{\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\right)
]

Steeper uphill slopes result in faster fire spread due to convective heating.

### 4. Fuel Moisture Approximation

Fuel moisture is estimated from atmospheric conditions:

[
FuelMoisture = f(RelativeHumidity, Temperature, Rainfall)
]

Lower fuel moisture increases ignition probability and flame intensity.

### 5. Fire Intensity (Byram Fireline Intensity)

Used to estimate the energy released along the fire front:

[
I = H \times W \times R
]

Where:

* (H): Heat content of fuel
* (W): Fuel consumed
* (R): Rate of Spread

### 6. Physics-Informed Loss Function

The model minimizes both prediction error and violations of physical fire behavior:

[
\mathcal{L}_{total}
===================

\mathcal{L}*{prediction}
+
\lambda
\mathcal{L}*{physics}
]

The physics loss penalizes predictions that contradict expected wildfire dynamics, such as rapid downhill spread without supporting wind conditions or unrealistic propagation through non-burnable terrain.

This hybrid approach enables PyroCast to generate forecasts that are both **data-driven** and **physically consistent**, improving robustness and interpretability for operational decision-making.
