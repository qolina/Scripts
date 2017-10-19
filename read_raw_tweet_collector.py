# this program is used to read raw tweet downloaded by 
# Twitter_dataset_collector (socialsensor version).
# not json by twitter_corpus_tools

import time
import argparse
import cPickle

# format: isTweetCode() + SEPARATOR + id + SEPARATOR + username + SEPARATOR + tweetText + SEPARATOR + pubTime + SEPARATOR + numRetweets + SEPARATOR + numFavorites + SEPARATOR + originalId;
# eg:   200    false   false   false   2193    O   315986582459019264  danisandland    @Gemasandy:If the whole world smoked a joint at the same time,Ther wud b world peace 4 at least 2 hours. Followed by a global food shortage.    5:40 PM - 24 Mar 2013   1   0   null 
def read_raw_tweet(input_filename):
    tweet_hash = {} # tweet_id: tweet_text
    tweet_feature_hash = {} # tweet_id: [user_name/user_id, time, retweet_num, favor_num]
    
    input_file = file(input_filename, "r")
    content = input_file.readlines()
    content = [line.strip().split("\t") for line in content]

    # filter out null tweet
    content = [arr for arr in content if arr[8]!="null"]
    for arr in content:
        if len(arr) != 13: continue
        tweet_id = arr[6]
        user_name = arr[7]
        tweet_text = arr[8]
        pub_time = from_format_time(arr[9])
        retweet_num = int(arr[10])
        favor_num = (arr[11])

        tweet_hash[tweet_id] = tweet_text
        tweet_feature_hash[tweet_id] = [user_name, pub_time, retweet_num, favor_num]
    print "## Loading done tweets.", time.asctime(), "  #tweet", len(tweet_hash)
    return tweet_hash, tweet_feature_hash
        

def from_format_time(time_str):
    #Time format in tweet: "4:32 AM - 17 Feb 2013 from Eden, England"
    if time_str.find("from") > 0:
        #time_zone = time_str[time_str.find("from"):]
        time_str = time_str[:time_str.find("from")].strip()
    input_time_format = r"%I:%M %p - %d %b %Y"
    pub_time_struct = time.strptime(time_str, input_time_format)
    return pub_time_struct

def to_format_time(time_struct):
    #Time format in tweet: "5:40 PM - 24 Mar 2013"
    out_time_format = r"%-I:%-M %p - %-d %b %Y"
    pub_time = time.strftime(out_time_format, time_struct)
    return pub_time

def get_arg():
    arg_parser = argparse.ArgumentParser(description="Read raw tweet downloaded by twitter_dataset_collector.")

    arg_parser.add_argument('input', help="Raw input tweet file")
    arg_parser.add_argument('-text_output', help="Raw input tweet file")

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_arg()
    
    tweet_hash, tweet_feature_hash = read_raw_tweet(args.input)

    if args.text_output is not None:
        outfile = open(args.text_output, "w")
        for tweet_id in sorted(tweet_hash.keys()):
            outfile.write(tweet_hash[tweet_id] + "\n")
        outfile.close()

        id_outfile = open(args.text_output+".id.cpickle", "w")
        cPickle.dump(sorted(tweet_hash.keys()), id_outfile)
        id_outfile.close()

