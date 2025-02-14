"""
This is script which fetch tweets from twitter apis based on user input query and perform sentiment analysis to determine tweet is positive, negative or neutral 

Library used 

==> tweepy : used for interact with twitter  
==> textblob : used for processing of textual data 
==> NLTK corpora : set of larget and structured texts

"""

import tweepy 
import re 
import textblob 


class TwitterSentimentAnalysis: 
    '''
    This is twitter sentiment class which contains properties and methods to perform sentiment analysis of tweets 
    
    '''
    
    def _init__(self):
        '''
        Credentials for twitter app 
        '''
        self._consumer_key =  "Your consumer key"
        self._consumer_secret = "Your consumer secret key" 
        self._access_token = "Your access token" 
        self._access_token_secert = "Your secret access token" 
        self._auth = None
        self._api = None
        self._tweets = []
        self._positive = []
        self._negative = []
        self._netural = [] 

    
    def _authorize_(self):
        '''
        This is utility function to verify user credentails and
        create instance of twitter api object to interact with twitter
        '''
        try:
            self._auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
            self._auth.set_access_token(self._access_token, self._access_token_secert)
            self._api = tweepy.API(self._auth)
        except:
            print("401 Invalid Credentials!")
            exit(1)


    
    def _sentize_tweet(self, tweet):
        '''
        Function to sentize tweet. it remove links, special characters and other invalid characters using regix statement
        '''
        return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", tweet).split())
    


    def _sentiment_tweet(self, tweet):
        filter_tweet = textblob(self._sentize_tweet(tweet))
        return filter_tweet.sentiment.polarity 
    

    def _fetch_tweets(self, query):
        '''
        function to get tweets from twitter api based on query

        '''

        try:
           
            tweets_list = self._api.search(q = query, count = 5)
            
            for tweet in tweets_list:

                process_tweet = {}
                process_tweet['text'] = tweet.text 
                process_tweet['sentiment'] = self._sentiment_tweet(tweet.text)
                
                if self._tweets.length > 0 and process_tweet not in self._tweets:
                    self._tweets.append(process_tweet) 
                else:
                    self._tweets.append(process_tweet) 
                     
        except Exception:
            print("Unable to fetch tweets")
            exit(0) 


    def app(self):
        '''
        Main handler for app working
        '''
        query = input("Enter your search word ")
        self._fetch_tweets(query)
        
        self._positive = [tweet for tweet in self._tweets if tweet['sentiment'] > 0]
        self._negative = [tweet for tweet in self._tweets if tweet['sentiment'] < 0]
        self._netural = [tweet for tweet in self._tweets if tweet['sentiment'] == 0]

        total = len(self._tweets)

        pos_percentage = 100 * len(self._positive) / total 
        neg_percentage = 100 * len(self._negative) / total 
        net_percentage = 100 * (total - (len(self._negative) + len(self._positive))) / total

        print(f"Postive Tweets Prcentage: {pos_percentage}% ")
        print(f"Negative Tweets Prcentage: {neg_percentage}% ")
        print(f"Netural Tweets Prcentage: {net_percentage}% ")


        print("Postive tweets are following: ")
        
        for postive in self._positive:
            print(postive['text'])

        print("Negative tweets are following: ")
        
        for negative in self._negative:
            print(negative['text'])

        print("Netural tweets are following: ")
        
        for netural in self._netural:
            print(netural['text'])


if __name__ == "__main__":
    app = TwitterSentimentAnalysis()
    app.app()