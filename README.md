How to run
1. pip install numpy
2. pip install scipy
3. pip install sklearn
4. python main.py

How to use
1. Task 1
2. Task 2
3. Task 3
4. Task 4
5. Task 5
6. Load data
7. Sample input
8. Quit

Task 1 calculates k similar users to the given user based on given textual model. 
Input: user_id model(TF, DF, TF-IDF) k

Task 2 calculates k similar images to the given image based on given textual model. 
Input: image_id model(TF, DF, TF-IDF) k

Task 3 calculates k similar locations to the given location based on given textual model. 
Input: location_id model(TF, DF, TF-IDF) k

Task 4 calculates k similar locations to the given location based on given visual model.
Input: location_id model(CM, CM3x3, CN, CN3x3, CSD, GLRLM, GLRLM3x3, HOG, LBP, LBP3x3) k

Task 5 calculates k similar locations to the given location based on all visual model.
Input: location_id k

Task 6 Loads textual and visual descriptors data to MongoDB
Input: path to the dataset

Task 7 prints output for the the given sample input