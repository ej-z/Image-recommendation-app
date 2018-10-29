How to run
1. pip install -r requirements.txt
2. python main.py

How to use
1. Task 1
2. Task 2
3. Task 3
4. Task 4
5. Task 5
6. Task 6
7. Task 7
8. Load data
0. Quit

Task 1 calculates k similar users to the given user based on given textual model. 
Input: user_id model(TF, DF, TF-IDF) k

Task 2 calculates k similar images to the given image based on given textual model. 
Input: image_id model(TF, DF, TF-IDF) k

Task 3 calculates k similar locations to the given location based on given textual model. 
Input: location_id model(TF, DF, TF-IDF) k

Task 4 calculates k similar locations to the given location based on given visual model.
Input: location_id model(CM, CM3x3, CN, CN3x3, CSD, GLRLM, GLRLM3x3, HOG, LBP, LBP3x3) k

Task 5 calculates k similar locations to the given location based on all visual models.
Input: location_id k

Task 6 prints k latent semantics using SVD algorithm for the location - location similarity matrix the the given sample input
Input k

Task 7 prints non overlapping groups of user, images and locations output based on k latent semantics for the the given sample input
Input k

Option 8 Loads textual and visual descriptors data to MongoDB
Input: path to the dataset

