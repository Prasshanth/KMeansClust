'''
A Python script to cluster Twitter tweets using the K-Means Clustering algorithm
Authors: Kannan Prasshanth Srinivasan, Sachin Kamasetty Venkatesha
Date: 16th April, 2017
'''
import json
import sys

#variable for holding the distances between points
POINT_DISTANCE = {}

def word_counts(word_list):
    '''
    Function which takes a list of words and returns a dictionary of the words and their counts
    Input: A list of words
    Output: A dictionary, with words as keys, and their counts as values
    '''
    #dictionary which stores the counts
    counts = {}
    #if word exists in dictionary, increment it's count, otherwise add the word to the dictionary
    for word in word_list:
        if word in counts:
            counts[word] = counts[word] + 1
        else:
            counts[word] = 1
    return counts

def dict_length(dictionary):
    '''
    Function which takes a dictionary with keys as strings, and values as integers, and
    returns the sum of the integers
    Input: A dictionary, with values as integers
    Output: Sum of all the values
    '''
    #variable which stores the sum
    length = 0
    for key in dictionary:
        length = length + dictionary[key]
    return length

def intersection(bucket_1, bucket_2):
    '''
    Function for calculating the size of the intersection of two multisets.
    Input: Two dictionaries, with keys as words, and the count of words as Value
    Output: An integer, which is the size of the intersection
    '''
    #variable for holding the result
    result = 0
    #for every word in bucket_a, check if word exists in bucket_b, and increment the result if so
    for word in bucket_1:
        while bucket_1[word] != 0 and word in bucket_2:
            if word in bucket_2:
                #decrement the counts of the word
                bucket_2[word] = bucket_2[word] - 1
                bucket_1[word] = bucket_1[word] - 1
                #pop the word from the buckets if their counts are 0
                if bucket_2[word] == 0:
                    bucket_2.pop(word, None)
                #increment the result
                result += 1
    return result

def union(bucket_1, bucket_2):
    '''
    Function for calculating the size of the union of two multisets.
    Input: Two dictionaries, with keys as words, and the count of words as Value
    Output: An integer, which is the size of the intersection
    '''
    #variable for holding the result
    result = 0
    #for every word in bucket_a and bucket_b, add the max of their counts
    for word in bucket_1:
        if word in bucket_2:
            #print max(bucket_a[word], bucket_b[word])
            result = result + max(bucket_1[word], bucket_2[word])
            bucket_2.pop(word, None)
        else:
            result = result + bucket_1[word]
    for word in bucket_2:
        result = result + bucket_2[word]
    return result


def jaccard_distance(tweet_a, tweet_b):
    '''
    Function for calculating the Jaccard distance between two tweets
    Inputs: Two lists of strings, each containing the words of the particular tweet
    Output: A floating point value, the Jaccard distance between the tweets
    '''
    #Bucket for words from Tweet A
    bucket_a = word_counts(tweet_a)
    #Bucket for words from Tweet B
    bucket_b = word_counts(tweet_b)
    #variable for storing the union:
    #bucket_a = set(tweet_a)
    #bucket_b = set(tweet_b)
    bucket_union = union(dict(bucket_a), dict(bucket_b))
    #variable for storing the intersection:
    bucket_intersect = intersection(dict(bucket_a), dict(bucket_b))
    #bucket_union = len(bucket_a.union(bucket_b))
    #bucket_intersect = len(bucket_a.intersection(bucket_b))
    #print bucket_a
    #print bucket_b
    #print bucket_intersect
    #print bucket_union
    return 1.0 - bucket_intersect*1.0/bucket_union

def assign_clusters(tweet_centroids, tweet_data):
    '''
    Function which assigns tweets to clusters, according to distance to closest centroid
    Input: a dictionary of cluster IDs as keys and Centroid Tweet IDs as values, and a dictionary
    with Tweet IDs as keys and Tweet Text as values
    Output: A dictionary with cluster IDs as keys and a list of Tweet IDs corresponding to each
    cluster as values
    '''
    #dictionary which stores the clusters
    clusters = {}
    #populate the dictionary with an empty list for every cluster
    for index in range(len(tweet_centroids)):
        clusters[index] = []
    #for every tweet, calculate jaccard distance to each centroid, and then
    #assign the tweet to the cluster of the nearest centroid
    #tweet_centroid_values = set(tweet_centroids.values())
    for tweet in tweet_data:
        #if tweet in tweet_centroid_values:
         #   continue
        min_jaccard_dist = 1
        cluster = 0
        for cent in tweet_centroids:
            dist_to_centroid = 1
            if (tweet_centroids[cent], tweet) not in POINT_DISTANCE:
                dist_to_centroid = jaccard_distance(tweet_data[tweet_centroids[cent]],
                                                    tweet_data[tweet])
                POINT_DISTANCE[(tweet_centroids[cent], tweet)] = dist_to_centroid
                POINT_DISTANCE[(tweet, tweet_centroids[cent])] = dist_to_centroid
            else:
                dist_to_centroid = POINT_DISTANCE[(tweet_centroids[cent], tweet)]
            if dist_to_centroid < min_jaccard_dist:
                min_jaccard_dist = dist_to_centroid
                cluster = cent
        clusters[cluster].append(tweet)
    return clusters

def calculate_centroid(cluster, tweet_data):
    '''
    Function which returns the centroid for a list of Tweets
    Input: a list of string Tweet IDs, a dictionary with tweet IDs as key and Tweet
     content as Values
    Output: a string Tweet ID
    '''
    #print cluster
    #variable for holding the current centroid
    cent = cluster[0]
    #variable for holding the current minimum mean distance
    min_distance = 1
    #for each tweet, calculate the mean distance to other tweets in the cluster, select
    #as centroid if the mean distance is less than the current minimum distance
    for tweet in cluster:
        total_distance = 0
        for other_tweet in cluster:
            if (tweet, other_tweet) not in POINT_DISTANCE:
                distance = jaccard_distance(tweet_data[tweet],
                                            tweet_data[other_tweet])
                total_distance = total_distance + distance
                POINT_DISTANCE[(tweet, other_tweet)] = distance
                POINT_DISTANCE[(other_tweet, tweet)] = distance
            else:
                total_distance = total_distance + POINT_DISTANCE[(tweet, other_tweet)]
        mean_distance = total_distance*1.0/len(cluster)
        if mean_distance < min_distance:
            min_distance = mean_distance
            cent = tweet
    return cent

def centroids(clusters, tweet_data):
    '''
    Function which returns the new centroids for a set of clusters given as input
    Input: a dictionary with cluster IDs as key, and a list of tweet IDs as value,
    a dictionary with tweet IDs as key and Tweet content as Values
    Output: A dictionary with cluster IDs as key and Tweet IDs as Values
    '''
    #Dictionary for holding the result centroids
    new_centroids = {}
    #for each cluster, calculate the centroid
    for cluster in clusters:
        new_centroids[cluster] = calculate_centroid(clusters[cluster], tweet_data)
    return new_centroids

def sse(clusters, centroid_values, tweet_data):
    '''
    Function which returns the SSE value for the given set of clusters and centroids
    Input: a dictionary with clusterIDs as key, and a list of tweet IDs as value, a dictionary with
    clusterIDs as key, and a Tweet ID as value, a dictionary with Tweet IDs as key, data as value
    Output: a floating point value which is the SSE
    '''
    #result variable
    result = 0
    #iterate through every cluster, add distance value of each tweet in cluster to cluster centroid
    for cluster in clusters:
        for tweet in clusters[cluster]:
            result += jaccard_distance(tweet_data[tweet], tweet_data[centroid_values[cluster]]) ** 2
    return result

#default values for number of clusters and tweets centroid file
NUM_CLUSTERS = 25
TWEET_CENTROID_FILE = "InitialSeeds.txt"

#Initializing tweets data file and the output file names
TWEETS_DATA_FILE = "Tweets.json"
OUTPUT_FILE = "tweets-k-means-output.txt"

#Get the command line arguments
ARGS = sys.argv

#if less than four arguments are given, use defaults
if len(ARGS) >= 5:
    NUM_CLUSTERS = int(ARGS[1])
    TWEET_CENTROID_FILE = ARGS[2]
    TWEETS_DATA_FILE = ARGS[3]
    OUTPUT_FILE = ARGS[4]
elif len(ARGS) == 4:
    print "Using default: "
    print "Output File: tweets-k-means-output.txt"
    NUM_CLUSTERS = int(ARGS[1])
    TWEET_CENTROID_FILE = ARGS[2]
    TWEETS_DATA_FILE = ARGS[3]
elif len(ARGS) == 3:
    print "Using defaults: "
    print "Tweets Data File: Tweets.json"
    print "Output File: tweets-k-means-output.txt"
    NUM_CLUSTERS = int(ARGS[1])
    TWEET_CENTROID_FILE = ARGS[2]
elif len(ARGS) == 2:
    print "Using defaults: "
    print "Tweets Centroid File: InitialSeeds.txt"
    print "Tweets Data File: Tweets.json"
    print "Output File: tweets-k-means-output.txt"
    NUM_CLUSTERS = int(ARGS[1])
else:
    print "Using defaults: "
    print "Number of clusters: 25"
    print "Tweets Centroid File: InitialSeeds.txt"
    print "Tweets Data File: Tweets.json"
    print "Output File: tweets-k-means-output.txt"

#Dictionary for holding the Tweets
TWEET_DATA = {}
#Dictionary for holding the raw Tweets
TWEET_CONTENT = {}

#Load the tweet data from the tweet data file, the individual tweet IDs are the keys
with open(TWEETS_DATA_FILE) as tweet_data_file:
    for line in tweet_data_file:
        TWEET = json.loads(line)
        TWEET_DATA[str(TWEET["id"])] = TWEET["text"].split()
        TWEET_DATA[str(TWEET["id"])] = TWEET["text"]

#Dictionary for holding the centroid tweets
TWEET_CENTROIDS = {}

#Load the centroid information for the centroid data file
with open(TWEET_CENTROID_FILE) as tweet_centroid_file:
    CENTROIDS = tweet_centroid_file.read().rsplit(",\n")
    #If number of centroids in the centroid data file is less than the number of clusters,
    #raise an error and exit
    if len(CENTROIDS) < NUM_CLUSTERS:
        print "Error: Number of centroids in Initial Seeds File less than number of clusters"
        sys.exit(1)
    for idx in range(0, NUM_CLUSTERS):
        TWEET_CENTROIDS[idx] = CENTROIDS[idx]


#print TWEET_DATA["323906483584655360"]
#print jaccard_distance(TWEET_DATA["323906483584655360"], TWEET_DATA["323906483584655360"])
#print jaccard_distance(["Hello", "World"], ["yoko", "ono"])
#Perform the algorithm until the centroid list does not change
ITER_NUMBER = 0
while True:
    print "Iteration number: " + str(ITER_NUMBER)
    #Dictionary with cluster number as key and the list of tweet IDs in the cluster as value
    CLUSTERS = assign_clusters(TWEET_CENTROIDS, TWEET_DATA)
    #print CLUSTERS
    NEW_CENTROIDS = centroids(CLUSTERS, TWEET_DATA)

    print "SSE: " + str(sse(CLUSTERS, NEW_CENTROIDS, TWEET_DATA))
    #print CLUSTERS
    #print NEW_CENTROIDS
    if NEW_CENTROIDS == TWEET_CENTROIDS:
        #print CLUSTERS
        #print "Converged"
        break
    else:
        TWEET_CENTROIDS = NEW_CENTROIDS
    ITER_NUMBER += 1

#Print everything to file:
FILE_OUTPUT = open(OUTPUT_FILE, 'w')
FILE_OUTPUT.write("SSE Value: ")
FILE_OUTPUT.write(str(sse(CLUSTERS, NEW_CENTROIDS, TWEET_DATA)))
FILE_OUTPUT.write("\n\nClusters:\n")
for cluster in CLUSTERS:
    FILE_OUTPUT.write(str(cluster))
    FILE_OUTPUT.write("\t")
    for tweet in CLUSTERS[cluster]:
        FILE_OUTPUT.write(tweet)
        FILE_OUTPUT.write(", ")
    FILE_OUTPUT.write("\n")

