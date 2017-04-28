# KMeansClust
A utility for implementing the K-Means Clustering algorithm on Tweets

This utility implements the K-Means Clustering algorithm for tweets provided to it. Tweets are provided to it in the form of JSON files, along with an initial seeds file, which contains the list of initial centroids used by the algorithm. If the number of clusters wanted is less than the number of centroid in the seeds file, then the initial n seeds will be taken for computation.

Requirements: Python 2.7

Usage: 
Usage: python tweet-k-means.py <numberOfClusters> <initialSeedsFile> <TweetsDataFile> <outputFile>
None of the arguments are mandatory.
If the number of arguments is less than 4, then the following defaults are used, depending upon the number of arguments provided:
Number of clusters: 25
Tweets Centroid File: InitialSeeds.txt
Tweets Data File: Tweets.json
Output File: tweets-k-means-output.txt

The initial seeds file should be in the following format:
323906397735641088,
323906483584655360,
323906657333682176,
323907258301939713,
323909308188344320,
where each of the values are Tweet IDs in the provided Tweets JSON file.

The following experiments were run on the seeds file and tweets included:
python tweet-k-means.py 5 InitialSeeds.txt Tweets.json tweets-5k-means-output.txt 
Iteration number: 0
SSE: 38.1328390559
Iteration number: 1
SSE: 31.8423295522
Iteration number: 2
SSE: 29.7040528793
Iteration number: 3
SSE: 30.1379217178
Iteration number: 4

python tweet-k-means.py 10 InitialSeeds.txt Tweets.json tweets-10k-means-output.txt 
Iteration number: 0
SSE: 27.6204669587
Iteration number: 1
SSE: 24.3654685185
Iteration number: 2
SSE: 23.9414681121
Iteration number: 3
SSE: 23.1155093567

python tweet-k-means.py 15 InitialSeeds.txt Tweets.json tweets-15k-means-output.txt 
Iteration number: 0
SSE: 22.1009751165
Iteration number: 1
SSE: 18.4797406928
Iteration number: 2
SSE: 16.5689247673
Iteration number: 3
SSE: 16.2649945606

python tweet-k-means.py 20 InitialSeeds.txt Tweets.json tweets-20k-means-output.txt 
Iteration number: 0
SSE: 17.1979415997
Iteration number: 1
SSE: 14.9083444152
Iteration number: 2
SSE: 13.6035945834
Iteration number: 3
SSE: 13.3176840284

python tweet-k-means.py 25 InitialSeeds.txt Tweets.json tweets-25k-means-output.txt 
Iteration number: 0
SSE: 9.77649080113
Iteration number: 1
SSE: 9.30318225293
Iteration number: 2
SSE: 8.83320459772
Iteration number: 3
SSE: 8.83320459772


As can be seen, the Sum of Squared Error is seen to decrease with increase in the number of clusters.









