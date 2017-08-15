'''
Created on 9 Apr 2015

@author: frannie
'''

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import time
import sys
#import json
#import re

#Variables that contains the user credentials to access Twitter API 
access_token = "3145927964-Hz2e0TxvsIgwDGFuIUrqW1EmoUhMHKXPjTm3HGl"
access_token_secret = "fliAeOvEC25fj5rNeC7uI3jhRwbnm8fdhKnRe9jb1rokG"
consumer_key = "hlOH0HalLRnMGkFGLZmWGGRG6"
consumer_secret = "48DC9ToG9KXOaA26DIK4n6oie38LTelUguNbgn6YuxWHaCX29z"

keyword_list = [
'$MMM','$ABT','$ABBV','$ACN','$ACE','$ACT','$ADBE','$ADT','$AES','$AET',
'$AFL','$AMG','$A','$GAS','$APD','$ARG','$AKAM','$AA','$ALXN','$ATI',
'$ALLE','$ADS','$ALL','$ALTR','$MO','$AMZN','$AEE','$AAL','$AEP','$AXP',
'$AIG','$AMT','$AMP','$ABC','$AME','$AMGN','$APH','$APC','$ADI','$AON',
'$APA','$AIV','$AAPL','$AMAT','$ADM','$AIZ','$T','$ADSK','$ADP','$AN',
'$AZO','$AVGO','$AVB','$AVY','$BHI','$BLL','$BAC','$BK','$BCR','$BAX',
'$BBT','$BDX','$BBBY','$BRK.B','$BBY','$BIIB','$BLK','$HRB','$BA','$BWA',
'$BXP','$BSX','$BMY','$BRCM','$BF.B','$CHRW','$CA','$CVC','$COG','$CAM',
'$CPB','$COF','$CAH','$HSIC','$KMX','$CCL','$CAT','$CBG','$CBS','$CELG',
'$CNP','$CTL','$CERN','$CF','$SCHW','$CHK','$CVX','$CMG','$CB','$CI',
'$XEC','$CINF','$CTAS','$CSCO','$C','$CTXS','$CLX','$CME','$CMS','$COH',
'$KO','$CCE','$CTSH','$CL','$CMCSA','$CMA','$CSC','$CAG','$COP','$CNX',
'$ED','$STZ','$GLW','$COST','$CCI','$CSX','$CMI','$CVS','$DHI','$DHR',
'$DRI','$DVA','$DE','$DLPH','$DAL','$XRAY','$DVN','$DO','$DTV','$DFS',
'$DISCA','$DISCK','$DG','$DLTR','$D','$DOV','$DOW','$DPS','$DTE','$DD',
'$DUK','$DNB','$ETFC','$EMN','$ETN','$EBAY','$ECL','$EIX','$EW','$EA',
'$EMC','$EMR','$ENDP','$ESV','$ETR','$EOG','$EQT','$EFX','$EQIX','$EQR',
'$ESS','$EL','$ES','$EXC','$EXPE','$EXPD','$ESRX','$XOM','$FFIV','$FB',
'$FDO','$FAST','$FDX','$FIS','$FITB','$FSLR','$FE','$FISV','$FLIR','$FLS',
'$FLR','$FMC','$FTI','$F','$FOSL','$BEN','$FCX','$FTR','$GME','$GCI',
'$GPS','$GRMN','$GD','$GE','$GGP','$GIS','$GM','$GPC','$GNW','$GILD',
'$GS','$GT','$GOOGL','$GOOG','$GWW','$HAL','$HBI','$HOG','$HAR','$HRS',
'$HIG','$HAS','$HCA','$HCP','$HCN','$HP','$HES','$HPQ','$HD','$HON',
'$HRL','$HSP','$HST','$HCBK','$HUM','$HBAN','$ITW','$IR','$TEG','$INTC',
'$ICE','$IBM','$IP','$IPG','$IFF','$INTU','$ISRG','$IVZ','$IRM','$JEC'
]

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        #decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        #created_at = decoded['created_at']
        #text = decoded['text'].encode('ascii', 'ignore')
        #text = re.sub(r'\s+', ' ', text).strip()
        #print '%s\t%s' % (created_at, text)
        
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authentication and the connection to Twitter Streaming API
    delay_sec = 60

    while True:
        try:
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = Stream(auth, l)
            #This line filter Twitter Streams to capture data by the keywords: e.g. 'python', 'javascript', 'ruby'
            stream.filter(track=keyword_list, languages=['en'])    
        except IOError, ex:
            timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print >> sys.stderr, '%s ERROR : %s' % (timestr, ex)
            time.sleep(delay_sec)
