#-*-coding:utf8;-*-
#qpy:console

import urllib.request as ur
from bs4 import BeautifulSoup, NavigableString, Tag
import csv
import re
import scipy
from scipy import stats
import numpy as np
import math

def binomialprob(n,k,p):
    num = math.factorial(n)
    d = n - k
    den = math.factorial(k)*math.factorial(d)
    C = num/den
    a = p**(k)
    e = 1 - p
    b = e**(d)
    prob = C*a*b
    return prob
    
def cumul_binom_prob(n,k,p):
    prob = 0
    i = 0
    while i <= k:
        num = math.factorial(n)
        d = n - i
        den = math.factorial(i)*math.factorial(d)
        C = num/den
        #print(C)
        a = p**(i)
        #print(a)
        e = 1 - p
        b = e**(d)
        #print(b)
        prob += C*a*b
        #print('p(' + str(i) + ')=')
        #print(prob)
        i += 1
    
    return prob

url = 'https://afltables.com/afl/teams/fremantle/allgames.html'

# Open the URL
page = ur.Request(url)
result = ur.urlopen(page)

# Store the HTML page in a variable
resulttext = result.read()

# Creates a nested data structure

soup = BeautifulSoup(resulttext, 'html.parser')
# Search for all in that table class in the soup

soup = soup.find_all(class_="sortable")
#Extract all data in the table from first element
trending_list = soup

#print(trending_list)

alldata = []
for line in trending_list: 
    seasondata = []   
    for tr in line:
        for row in tr:
            k=0
            data = []
            for i in row:                    
                if k > 0:
                    for td in i:
                        data.append(td)                                                        
                                                                      
                k+=1
            h = len(data)                
            if h > 0:
                seasondata.append(data)
    alldata.append(seasondata)

allgames = []
for season in alldata:
    for game in season:
        if game[0] == 'H' or game[0] == 'A':
            allgames.append(game)

#print(alldata)  


for game in allgames:
    element = game[4]
    if(isinstance(element, Tag)):
        for i in element:
            game[4] = i        

#print(allgames)

allfreoscores = []
allopponentscores = []
allmargins = []

allfreoscores_home = []
allopponentscores_home = []
allmargins_home = []

allfreoscores_away = []
allopponentscores_away = []
allmargins_away = []

games = 0
wins = 0
losses = 0
draws = 0

for game in allgames:
    games += 1
    freo = str(game[3])
    freo = int(freo)
    other = str(game[5])
    other = int(other)
    margin = str(game[7])
    margin = int(margin)
    allfreoscores.append(freo)
    allopponentscores.append(other)
    allmargins.append(margin)
    if margin > 0:
        wins += 1
    if margin < 0:
        losses += 1
    if margin == 0:
        draws += 1
    if game[0] == 'H':
        allfreoscores_home.append(freo)
        allopponentscores_home.append(other)
        allmargins_home.append(margin)
    if game[0] == 'A':
        allfreoscores_away.append(freo)
        allopponentscores_away.append(other)
        allmargins_away.append(margin)

output_csv = '/storage/emulated/0/Documents/FreoScores.csv'
csvfile = open(output_csv, 'w')
csvfile.write('H or A, Opponent, Scoring Freo, Freo Final Score, Scoring Opponent, Other Final Score, Result, Margin, Freo WDL, Venue, Crowd, Date\n')
for game in allgames:
    for x in game:
        csvfile.write(str(x) + ',')
    csvfile.write('\n')
csvfile.close()
     
print ('Fremantle')
print ('Played ' + str(games))
print ('Won ' + str(wins))
print ('Lost ' + str(losses))
print ('Drawn ' + str(draws))

n = 22
p = wins/games

k = input('How many games can Freo win?: ')
k = int(k)

probabilityk = 1 - cumul_binom_prob(n,k,p)

print('Based on historical Freo data')
print('The probability of Freo winning')
print('(At least)')
print(str(k) + ' games: ' + str(probabilityk))


score = input ('Enter a score for Freo: ')
score = int(score)
opp_score = input('Enter a score for Freo opponent: ')
opp_score = int(opp_score)
margin = score - opp_score

allfreoscores = np.array(allfreoscores)
allopponentscores = np.array(allopponentscores)
allmargins = np.array(allmargins)

allfreoscores_home = np.array(allfreoscores_home)
allopponentscores_home = np.array(allopponentscores_home)
allmargins_home = np.array(allmargins_home)

allfreoscores_away = np.array(allfreoscores_away)
allopponentscores_away = np.array(allopponentscores_away)
allmargins_away = np.array(allmargins_away)

mean_allfreoscores = np.mean(allfreoscores)
mean_allopponentscores = np.mean(allopponentscores)
mean_allmargins = np.mean(allmargins)

sd_allfreoscores = np.std(allfreoscores)
sd_allopponentscores = np.std(allopponentscores)
sd_allmargins = np.std(allmargins)

mean_allfreoscores_home = np.mean(allfreoscores_home)
mean_allopponentscores_home = np.mean(allopponentscores_home)
mean_allmargins_home = np.mean(allmargins_home)

sd_allfreoscores_home = np.std(allfreoscores_home)
sd_allopponentscores_home = np.std(allopponentscores_home)
sd_allmargins_home = np.std(allmargins_home)

mean_allfreoscores_away = np.mean(allfreoscores_away)
mean_allopponentscores_away = np.mean(allopponentscores_away)
mean_allmargins_away = np.mean(allmargins_away)

sd_allfreoscores_away = np.std(allfreoscores_away)
sd_allopponentscores_away = np.std(allopponentscores_away)
sd_allmargins_away = np.std(allmargins_away)

z_freoscore = (score-mean_allfreoscores)/(sd_allfreoscores)
z_freoscore_h = (score-mean_allfreoscores_home)/(sd_allfreoscores_home)
z_freoscore_a = (score-mean_allfreoscores_away)/(sd_allfreoscores_away)

z_oppscore = (opp_score-mean_allopponentscores)/(sd_allopponentscores)
z_oppscore_h = (opp_score-mean_allopponentscores_home)/(sd_allopponentscores_home)
z_oppscore_a = (opp_score-mean_allopponentscores_away)/(sd_allopponentscores_away)

z_margin = (margin-mean_allmargins)/(sd_allmargins)
z_margin_h = (margin-mean_allmargins_home)/(sd_allmargins_home)
z_margin_a = (margin-mean_allmargins_away)/(sd_allmargins_away)

print('Calculating Probabilities')
cdf_value_fs = stats.norm(loc = 0 , scale = 1).cdf(z_freoscore)
prob_fs = 1 - cdf_value_fs
cdf_value_fsh = stats.norm(loc = 0 , scale = 1).cdf(z_freoscore_h)
prob_fsh = 1 - cdf_value_fsh
cdf_value_fsa = stats.norm(loc = 0 , scale = 1).cdf(z_freoscore_a)
prob_fsa = 1 - cdf_value_fsa

print('The probability that Freo will score ' + str(score) + ' or more is approx. ' + str(prob_fs))
print('For home games this probability is approx. ' + str(prob_fsh))
print('For away games this probability is approx. ' + str(prob_fsa))

cdf_value_os = stats.norm(loc = 0 , scale = 1).cdf(z_oppscore)
prob_os = cdf_value_os
cdf_value_osh = stats.norm(loc = 0 , scale = 1).cdf(z_oppscore_h)
prob_osh = cdf_value_osh
cdf_value_osa = stats.norm(loc = 0 , scale = 1).cdf(z_oppscore_a)
prob_osa = cdf_value_osa 

print('The probability that Freo will concede ' + str(opp_score) + ' or less is approx. ' + str(prob_os))
print('For home games this probability is approx. ' + str(prob_osh))
print('For away games this probability is approx. ' + str(prob_osa))

cdf_value_m = stats.norm(loc = 0 , scale = 1).cdf(z_margin)
prob_m = 1 - cdf_value_m
cdf_value_mh = stats.norm(loc = 0 , scale = 1).cdf(z_margin_h)
prob_mh = 1 - cdf_value_mh
cdf_value_ma = stats.norm(loc = 0 , scale = 1).cdf(z_margin_a)
prob_ma = 1 - cdf_value_ma 

print('The probability that the margin will be ' + str(margin) + ' or more is approx. ' + str(prob_m))
print('For home games this probability is approx. ' + str(prob_mh))
print('For away games this probability is approx. ' + str(prob_ma))
