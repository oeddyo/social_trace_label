# This is a container set for each annotator
import os
import random
import json


class Annotator:
    def __init__(self):

        cur_dir = os.path.dirname(os.path.realpath(__file__))
        tweets_file = os.path.join(cur_dir, 'static/tweets.txt')
        
        self.tweets = open(tweets_file).readlines()
        random.shuffle(self.tweets)
        
        self.condition = 0
        
        ppl_file = os.path.join(cur_dir, 'static/people.txt')
        
        # format: username, firname, lastname, image_url, avaratar_age
        self.people_list = [line.split(',') for line in open(ppl_file, 'r').readlines()[1:]]
        self.males = [line for line in self.people_list if line[3].find("female")==-1]   
        self.females = [line  for line in self.people_list if line[3].find("female")!=-1]

        self.gender = []
        self.mutual = []
        self.geo = []
        idx = 0

        condition_index = []
        for gender in range(2):
            for geo in range(2):
                for n_mutual in range(3):
                    condition_index.append( (gender, geo, n_mutual))
        random.shuffle(condition_index)
        for idx in condition_index:
            gender, geo, n_mutual = idx
            self.gender.append(gender)
            self.mutual.append(n_mutual)
            self.geo.append(geo)
        """
        # could also shuffle here
        for gender in range(2):
            for geo in range(2):
                for n_mutual in range(3):
                    self.gender.append(gender)
                    self.mutual.append(n_mutual)
                    self.geo.append(geo)
                    idx += 1 
        """
        self.n_condition = 12
    
    def get_geo(self, near_or_far):
        # 0 near, 1 far
        near = ['Ithaca, NY', 'New York, NY', 'Boston, MA', 'Syracuse, NY']
        far = ['San Francisco, CA', 'Austin, TX', 'Maiami, FL', 'Seattle, WA']
        
        rd1 = random.randint(0, 2)
        rd2 = random.randint(0, 2)
        
        if near_or_far == 0:
            return near[rd1]
        else:
            return far[rd2]
    
    def get_post_user(self, male_or_female):
        # 0 male, 1 female
        if male_or_female == 0:
            # male
            rd = random.randint(0, len(self.males)-1)
            return self.males[rd]
        else:
            # female
            rd = random.randint(0, len(self.females)-1)
            return self.females[rd]
    
    def get_random_retweeter_avartars(self, n, gender ):
        urls = []
        n_male = None
        n_female = None

        if n<=3:
            if gender == 0:
                n_male = n
                n_female = 0
            else:
                n_female = n
                n_male = 0
        else:
            if gender == 0:
                n_male = random.randint(n/2 + 2, max(n/2+1, n) )
                n_female = n - n_male
            elif gender == 1:
                n_female = random.randint(n/2 + 2, max(n/2 + 1, n) )
                n_male = n - n_female

        print 'retweeters male = ', n_male, 'female = ', n_female
        for i in range(n_male):
            link = './static/'+self.get_post_user(0)[3]
            if link in urls: # heruistic avoid duplicate
                link = './static/'+self.get_post_user(0)[3]
            urls.append(link)
        for i in range(n_female):
            link = './static/'+self.get_post_user(1)[3]
            if link in urls: # heruistic avoid duplicate
                link = './static/'+self.get_post_user(1)[3]
            urls.append(link)
        random.shuffle(urls)
        return n_male, n_female, urls

    def get_next(self, ):
        # logic controling conditions here
        if self.condition >= self.n_condition:
            return None
        mutual = [0 + random.randint(0, 2) , 5 + random.randint(-1, 1), 10 + random.randint(-1, 1)]
        mutual = [max(0, i) for i in mutual ]
        gender = self.get_post_user(self.gender[self.condition])
        user_name = gender[0]
        first_name = gender[1]
        last_name = gender[2]
        avartar_url = './static/'+gender[3]
        avartar_age = gender[4]

        tweet_text = self.tweets[self.condition]
        mutual = mutual[self.mutual[self.condition]] 
        geo = self.get_geo(self.geo[self.condition])
        gender_of_retweeters = self.gender[self.condition]
        print 'gender this time = ', gender_of_retweeters 

        n_male_retweeter, n_female_retweeter, retweeters_avartars = self.get_random_retweeter_avartars(mutual, gender_of_retweeters) 

        json_obj = {'condition':self.condition, 
                'user_name':user_name, 
                'first_name':first_name, 
                'last_name':last_name, 
                'avartar_url':avartar_url, 
                'geo':geo,
                'mutual':mutual,
                'text': tweet_text,
                'retweeters': retweeters_avartars[:mutual],
                'n_male_retweeter':n_male_retweeter,
                'n_female_retwetter':n_female_retweeter
                }
        
        self.condition += 1 
        return json.dumps(json_obj) 
        
        #return self.condition, user_name, first_name, last_name, avartar_url, geo, mutual

def test():
    annotator = Annotator()
    while 1:
        tmp = annotator.get_next()
        if tmp == None:
            break
        print tmp
