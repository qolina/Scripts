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

#Variables that contains the user credentials to access Twitter API 
access_token = "3145927964-4AaPsN4mlIQK58bT1xUj3uWxJArjeWsv70pATbA"
access_token_secret = "Vcpfd3yXFbB2JEZMh4quZKiL9Dn728HLoledDshTenXwb"
consumer_key = "mxgUoVpLZSici26FO9FlMRvyd"
consumer_secret = "woBwMsKwAZ8wLH0vtrLELqhvXdnxnRigMX6dBhusKttdVdU1Kj"

keyword_list = [
'$JNJ','$JCI','$JOY','$JPM','$JNPR','$KSU','$K','$KEY','$GMCR','$KMB',
'$KIM','$KMI','$KLAC','$KSS','$KRFT','$KR','$LB','$LLL','$LH','$LRCX',
'$LM','$LEG','$LEN','$LVLT','$LUK','$LLY','$LNC','$LLTC','$LMT','$L',
'$LO','$LOW','$LYB','$MTB','$MAC','$M','$MNK','$MRO','$MPC','$MAR',
'$MMC','$MLM','$MAS','$MA','$MAT','$MKC','$MCD','$MHFI','$MCK','$MJN',
'$MWV','$MDT','$MRK','$MET','$KORS','$MCHP','$MU','$MSFT','$MHK','$TAP',
'$MDLZ','$MON','$MNST','$MCO','$MS','$MOS','$MSI','$MUR','$MYL','$NDAQ',
'$NOV','$NAVI','$NTAP','$NFLX','$NWL','$NFX','$NEM','$NWSA','$NEE','$NLSN',
'$NKE','$NI','$NE','$NBL','$JWN','$NSC','$NTRS','$NOC','$NRG','$NUE',
'$NVDA','$ORLY','$OXY','$OMC','$OKE','$ORCL','$OI','$PCAR','$PLL','$PH',
'$PDCO','$PAYX','$PNR','$PBCT','$POM','$PEP','$PKI','$PRGO','$PFE','$PCG',
'$PM','$PSX','$PNW','$PXD','$PBI','$PCL','$PNC','$RL','$PPG','$PPL',
'$PX','$PCP','$PCLN','$PFG','$PG','$PGR','$PLD','$PRU','$PEG','$PSA',
'$PHM','$PVH','$QEP','$PWR','$QCOM','$DGX','$RRC','$RTN','$RHT','$REGN',
'$RF','$RSG','$RAI','$RHI','$ROK','$COL','$ROP','$ROST','$RCL','$R',
'$CRM','$SNDK','$SCG','$SLB','$SNI','$STX','$SEE','$SRE','$SHW','$SIAL',
'$SPG','$SWKS','$SLG','$SJM','$SNA','$SO','$LUV','$SWN','$SE','$STJ',
'$SWK','$SPLS','$SBUX','$HOT','$STT','$SRCL','$SYK','$STI','$SYMC','$SYY',
'$TROW','$TGT','$TEL','$TE','$THC','$TDC','$TSO','$TXN','$TXT','$HSY',
'$TRV','$TMO','$TIF','$TWX','$TWC','$TJX','$TMK','$TSS','$TSCO','$RIG',
'$TRIP','$FOXA','$TSN','$TYC','$USB','$UA','$UNP','$UNH','$UPS','$URI',
'$UTX','$UHS','$UNM','$URBN','$VFC','$VLO','$VAR','$VTR','$VRSN','$VZ',
'$VRTX','$VIAB','$V','$VNO','$VMC','$WMT','$WBA','$DIS','$WM','$WAT',
'$ANTM','$WFC','$WDC','$WU','$WY','$WHR','$WFM','$WMB','$WIN','$WEC',
'$WYN','$WYNN','$XEL','$XRX','$XLNX','$XL','$XYL','$YHOO','$YUM','$ZMH',
'$ZION','$ZTS'
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
        #delay_sec = delay_sec + 60
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

