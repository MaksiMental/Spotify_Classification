# Predicting Song popularity using spotify audio features

The ability to predict a song’s popularity based on metadata and attributes holds significant industrial value. Our goal is to realize this through the application of machine learning techniques. We utilize data sourced from the Spotify Web API, encompassing information on over 120,0000. Necessary pre-processing is performed to facilitate the testing of various regression and classification algorithms. Based on the results obtained, we construct ensemble learning models for classification, fine-tuning them to yield optimal test outcomes. Our findings suggest that tree-based algorithms generally deliver competitive results. However, due to the imbalance in classification, the models demonstrate a higher proficiency in predicting non-popular songs, resulting in a substantial number of false negatives for popular ones.

## Results
Below are our results

```
| Model                      | Precision | Recall  | F1 Score |
|----------------------------|-----------|---------|----------|
| Voting Classifier          | 0.862935  | 0.847008| 0.854897 |
| XGBoost Under-sampled      | 0.876311  | 0.831579| 0.853359 |
| XGBoost Over-sampled       | 0.825533  | 0.859697| 0.842269 |
| Random Forest Under-sampled| 0.788168  | 0.618601| 0.693165 |
| Random Forest Over-sampled | 0.461708  | 0.875415| 0.604561 |
| Dummy Classifier           | 0.239006  | 1.000000| 0.385803 |

```

## Requirements

See requirements.txt for packages and versions (and below to install).

## Setup

Install the dependencies:

```bash
$ pip install -r requirements.txt
```

Locate the Code.ipybn and press run all
