# Disaster_response
Analyzing Disaster response massages pipeline to classify type of call

# Contents

[***Objective***](https://github.com/uriaLevko/Disaster_response#objective)

[***Overview***](https://github.com/uriaLevko/Disaster_response#overview)

[***Components***](https://github.com/uriaLevko/Disaster_response#Components)

[***Files***](https://github.com/uriaLevko/Disaster_response#files)

[***Results_discussion***](https://github.com/uriaLevko/Disaster_response#Results_discussion)

<p align="center">
<img src="statis/dis2.jpg" width=60% height=60% >
</p>

# Objective

* machine learning pipeline to categorize disaster events
* send the messages to an appropriate disaster relief agency
* disply results in webapp
* provide an API to improve Dataset (on progress)


# Overview

In this project, I analyzed disaster data provided by <a href='https://appen.com/'>Figure Eight</a> to build a model for an API that classifies disaster messages.

The Project dataset contained real messages that were sent during disaster events. 

The aim is creating a machine learning pipeline to categorize these events so that its possible to send the messages to an appropriate disaster relief agency.

The project includes a web app where an emergency worker can input a new message and get classification results in several categories.

Below are a few screenshots of the web app.


<table><tr>
<td> <img src="statis/sitetop.PNG" title="appup" style="width: 350px;"/> </td>
    <td></td><td></td>
<td> <img src="statis/sitedown.PNG" title="appdown" style="width: 250px;"/> </td>
    <td></td><td></td>
</tr></table>

# Components

There are three main components to this project.

1. ETL Pipeline - process_data.py:
* Loads the messages and categories datasets
* Merges the two datasets
* Cleans the data
* Stores it in a SQLite database

2. ML Pipeline - train_classifier.py, a machine learning pipeline that:
* Loads data from the SQLite database
* Splits the dataset into training and test sets
* Builds a text processing and machine learning pipeline
* Trains and tunes a model using GridSearchCV
* Outputs results on the test set
* Exports the final model as a pickle file
3. Flask Web App -
* classes data visualizations using Plotly in the web app.
* input massage to get class classification

# Files

# Results_discussion

<p align="center">
<img src="statis/newplot (1).png" width=100% height=100% >
</p>

## Unballanced situation
looking at the image above, it's clear we are dealing with a highly imballanced dataset where only 3 classes has more then 20% minority class ratio, and many classes are pretty much all labeled as False.
This is not an easy situation, and among the techniques to deal with it I would emphasize the following (there are meny any more): 
1. Data improvement:
* Undersampling the Majority Class
* Oversampling the Minority Class
* Combine Data Undersampling and Oversampling
* Cost-Sensitive Algorithms
* Feature engineering
2. Threshold-Moving for Imbalanced Classification:
* Converting Probabilities to Class Labels
* Threshold-Moving for Imbalanced Classification
* Optimal Threshold for ROC Curve
* Optimal Threshold for Precision-Recall Curve
* Optimal Threshold Tuning

At this point, no such techniques were used at this project, but I plan on improving the results in the near future.
## Precision vs. Recall
However, by undertanding that we are dealing with a highly imbalanced dataset, some point needs to be taken in considiration when analazig the current results:
1. We can't use accuracy as a metric as it will produce excelent results due to the imbalance
<p align="center">
<img src="statis/accuracy.PNG" width=50% height=50% title="99% accuracy with little to no effort">
</p>
2.according to the imbalance in class (positive or negative) to to the topic, we will have to choose the right metric:
 * Precision: Appropriate when minimizing false positives is the focus - apropriate classes that demand high reasource allocation but are not life saving.
 * Recall: Appropriate when minimizing false negatives is the focus - apropriate classes that are highly life saving.
 * F-Measure: provides a way to combine both precision and recall into a single measure that captures both properties.
3.no single threshold can be acticated for al classes, and we will have to change threshold according to:
 * Class imbalance (positive or negative).
 * Metric selection (logical class determines the metric).
 * use of ROC curves as indicators.
