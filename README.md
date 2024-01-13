# Predicting Wine Grape Varietal Suitability Based on Climate and Precipitation (WIP)

## Introduction

This project aims to create a machine learning model that estimates the suitability of various wine grape varietals for a specific location based on recent aggregated weather data. The model addresses the challenges posed by climate change to viticulture, serving as a tool for winemakers to assess the feasibility of cultivating different grape varieties or exploring new viticulture regions.

## Problem Space

- **The Impact of Climate Change**: Exploring how changing weather patterns affect traditional wine grape cultivation zones.
- **Adaptation and Sustainability**: Identifying new areas suitable for viticulture and adapting cultivation practices in response to climate change.
- **Predictive Analysis**: Developing a machine learning model to evaluate the viability of different grape varieties in varying climatic conditions.

## User Persona

- **Target Audience**: Wine producers and vineyard owners, especially those not constrained by appellation restrictions.
- **Benefits**: Aiding users in selecting the most suitable grape varieties for their locations and adapting to climate change effectively.
- **Sustainability**: Ensuring the sustainability of viticulture practices and maintaining wine quality amidst changing climate conditions.

## The Big Idea

- **Predictive Machine Learning Model**: Utilizing historical climate data to forecast the suitability of different grape varieties for viticulture.
- **Data-Driven Approach**: Training models on weather, sunlight exposure, and wine scores to capture the intricate effects of climate on wine production.
- **Leveraging Wine Scores**: Using median values of wine scores and significant sample sizes to minimize the bias of boutique winemaking.

## Project Impact

- **Climate Change Adaptation**: Assisting viticulturists in adapting to climate change by predicting future grape suitability.
- **Exploration of New Terroirs**: Encouraging the discovery of new viticulture areas, diversifying wine production.
- **Economic Growth**: Stimulating regional economic development through the introduction of new wine industries.
- **Global Wine Market**: Enhancing competitive quality and pricing by identifying untapped viticultural regions.

### Data Sources

- **Wine Data**: Primarily sourced from [Kaggle's wine review dataset](https://www.kaggle.com/datasets/zynicide/wine-reviews), initially scraped by [Zack Thoutt](https://github.com/zackthoutt) for his [wine deep learning project](https://github.com/zackthoutt/wine-deep-learning). Additional data obtained through a custom scraper targeting [Wine Enthusiast ratings](https://www.wineenthusiast.com/?s=&search_type=ratings&drink_type=wine).
- **Weather Data**: Obtained from [NOAA's historical climate and weather datasets](https://www.ncei.noaa.gov/products/world-weather-records), published by World Weather Records. The raw data, provided in unstructured .txt files, required the development of a custom parsing script to transform it into a structured .csv format suitable for data exploration and analysis.

## Additional Considerations

- **Holistic Understanding**: Recognizing that wine quality is influenced not only by climate but also by soil type, winemaking techniques, and other environmental elements.
- **Soil and Climate Synergy**: Considering scenarios where climate data suggests suitability, but soil conditions may require further analysis.
- **Focus on Broad Trends**: Concentrating on data that reflects general quality trends rather than individual outlier scores in wine ratings.

---
*This project is a work in progress and subject to continuous updates and improvements.*
