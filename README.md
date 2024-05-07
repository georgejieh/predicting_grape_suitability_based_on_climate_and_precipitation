# Predicting Wine Grape Varietal Suitability Based on Climate Data

## Introduction

As climate change reshapes traditional viticulture zones, understanding its impact is crucial for the sustainability and adaptation of wine production. This project develops a machine learning model to predict the suitability of different wine grape varietals based on climatic conditions. The aim is to aid wine producers and vineyard owners in selecting the most suitable grape varieties for their regions, considering the recent weather trends.

## Problem Statement

- **Impact of Climate Change**: How do changing weather patterns affect traditional wine grape cultivation areas?
- **Adaptation to Climate Variability**: Can winemakers identify new areas suitable for viticulture under changing climate conditions?
- **Predictive Analysis for Vineyard Management**: How can data-driven models forecast grape varietal suitability and inform viticultural practices?

## User Persona

The primary users of this model are wine producers and vineyard owners who seek to optimize grape selection and cultivation practices in response to climate variability. The model serves as a decision-support tool, providing insights that help maintain wine quality and vineyard productivity in a changing climate.

## Data Description

### Data Sources

- **Wine Data**: Compiled from Kaggle's wine review dataset and additional ratings from Wine Enthusiast. 
- **Weather Data**: Aggregated using the WWO Weather API, sourced via the Bing API for precise location-based weather data.

### Data Dictionaries

**Wine Data Dictionary**:
1. **Wine Name**: Name of the wine.
2. **Region**: Geographic area of wine production.
3. **Country**: Country of origin.
4. **Score**: Professional rating score.
5. **Price**: Retail price of the wine.
6. **Winery**: Producer of the wine.
7. **Variety**: Grape variety used.
8. **Vintage**: Harvest year of the wine grapes.

**Weather Data Dictionary**:
- **Hemisphere**: Hemisphere of the wine location (North/South).
- **Budburst and Early Growth (BEG)**, **Flowering, Fruit Set, and Veraison (FFV)**, **Harvest and Early Dormancy (HED)**, **Late Dormancy (LD)**: Seasonal divisions each encompassing multiple months relevant to vine growth cycles, each recorded with:
  - **tmax**: Highest air temperature (°C).
  - **tmin**: Lowest air temperature (°C).
  - **tavg**: Average air temperature (°C).
  - **prcp**: Total precipitation (mm).
  - **humidity**: Average relative humidity (%).
  - **sunhour**: Total sunlight hours.

## Methodology

### Exploratory Data Analysis (EDA)

Our EDA focused on visualizing wine scores, prices, and their relationships with weather parameters. Key findings include:
- Detailed labeling correlates with higher quality and price.
- Varietal and country-specific score distributions show significant variability, indicating diverse viticultural and winemaking practices.

### Modeling Approach

We utilized various machine learning models:
- **Initial Models**: Logistic Regression, Random Forest, Gradient Boosting Classifier, and Neural Networks.
- **Model Optimization**: AutoML tools (H2O, TPOT, AutoKeras) refined the models, with H2O's Distributed Random Forest achieving the best performance.

#### Challenges and Solutions
- **Data Quality**: Ensuring the accuracy of geocoordinate fetching and weather data was challenging. Improvements in API utilization and data handling were implemented.
- **Class Imbalance**: Applied SMOTE for oversampling and random under sampling to address imbalances, enhancing model performance.

## Final Presentation: Web Application

The project is encapsulated in a Flask web application that interacts with the H2O model. Users input an address and country; the app then predicts the suitability of each grape varietal based on the past year's weather data, then displays the top five grape varietals it is most confident in.

## Impact and Future Work

- **Climate Adaptation**: The tool assists viticulturists in adapting cultivation strategies based on predictive climate impact analysis.
- **Exploration of New Terroirs**: Encourages exploration of potentially viable new viticulture areas, fostering biodiversity and regional development.
- **Enhanced Decision Making**: Provides a data-driven approach for selecting grape varietals that are likely to thrive under projected climatic conditions.

Future enhancements will focus on integrating real-time climate forecasting and expanding the dataset to include more granular soil and topographic data, further refining the predictive capabilities of the model.

---
*This project is ongoing and subject to updates as new data and modeling techniques become available.*