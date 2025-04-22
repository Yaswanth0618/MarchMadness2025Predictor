March Madness 2025 Predictor
============================

Created: March 18, 2025  
Published to GitHub: April 21, 2025  
By: Yaswanth Kandra

Description:
------------
A machine learning-powered tool to predict NCAA basketball game outcomes based on team statistics.

Installation:
-------------
1. Clone this repository:
   - git clone https://github.com/Yaswanth0618/MarchMadness2025Predictor.git
   - cd MarchMadness2025Predictor

2. Install required Python packages:
   - pip install pandas
   - pip install joblib
   - pip install itertools
   - pip install scikit-learn
   - pip install numpy

Data Preparation:
----------------
1. Place your team data in CSV format at Data/team_2025.csv with these columns:
   Name,Rank,TournRank,ORating,ORank,DRating,DRank,TrapOfEx,KenPomTop,Both

2. Example Row:
   Duke,1,1,128,3,89.8,4,Yes,Yes,Yes

Usage:
------
1. Train the Model:
    - python src/train_model.py

2. Make Predictions:
    - python src/predict.py
    - Note: Copy names directly from the CSV's "Name" column to avoid errors while running predict.py


Sources For Data:
------
 - https://kenpom.com/
 - https://x.com/ryanhammer09/status/1901689323604304310
 - https://barttorvik.com/quadrants.php?sort=Q1&conlimit=All
 - https://www.reddit.com/r/CollegeBasketball/comments/1jeno4s/i_made_a_march_madness_2025_cheat_sheet_so_you/
