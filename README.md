# Covid19-Classification
This project aims to classify whether the patient is covid-19 based on clinical notes of patients' chest X-ray or CT images.

## Modeling
### Experiment 1: pre-trained BERT + fine tuning
#### 1) 

After deduplication (clinical notes) by 03-27-2020:

| Covid-19 | None-Covid-19 | Total |
| --- | --- | --- | 
| 92 | 14 | 106 |

Since label bias, manually constructed 27 extra fake None-Covid-19 cases.

| Covid-19 | None-Covid-19 | Total |
| --- | --- | --- | 
| 92 | 41 | 133 |

| | Covid-19 | None-Covid-19 | Total |
| ---| --- | --- | --- | 
| Training | 72 | 26 | 98 |
| Testing | 20 | 15 | 35 |

| | True(label) | False(label) | 
| ---| --- | --- | 
| True(pred) | TP=20 | FP=8 | 
| False(pred) | FN=0 | TN=7 | 

Precision = 20 / (20+8) = 0.71

Recall = 20 / (20 + 0) = 1

F1 = 0.83

#### 2) 

After deduplication (clinical notes) by 03-27-2020:

| Covid-19 | None-Covid-19 | Total |
| --- | --- | --- | 
| 92 | 14 | 106 |

Since label bias, manually copy 4 times of 14 original None-Covid-19 cases to get totally 70 None-Covid-19 cases.

| Covid-19 | None-Covid-19 | Total |
| --- | --- | --- | 
| 92 | 70 | 162 |

| | Covid-19 | None-Covid-19 | Total |
| ---| --- | --- | --- | 
| Training | 72 | 56 | 128 |
| Testing | 20 | 14 | 34 |

| | True(label) | False(label) | 
| ---| --- | --- | 
| True(pred) | TP=18 | FP=0 | 
| False(pred) | FN=2 | TN=14 | 

Precision = 18 / (18+0) = 1

Recall = 18 / (18 + 2) = 0.9

F1 = 0.94

#### 3) 

After deduplication (clinical notes) by 03-28-2020:

| Covid-19 | None-Covid-19 | Total |
| --- | --- | --- | 
| 104 | 37 | 141 |

| | Covid-19 | None-Covid-19 | Total |
| ---| --- | --- | --- | 
| Training | 83 | 22 | 105 |
| Testing | 21 | 15 | 36 |

| | True(label) | False(label) | 
| ---| --- | --- | 
| True(pred) | TP=19 | FP=10 | 
| False(pred) | FN=2 | TN=5 | 

Precision = 19 / (19+10) = 0.66

Recall = 19 / (19 + 2) = 0.9

F1 = 0.76
