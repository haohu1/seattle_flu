import pickle
import pandas as pd

from nltk.probability import FreqDist, MLEProbDist

KC_age_gender = pd.read_pickle('input/KC_CT_age_gender.pickle')
#print KC_age_gender

print KC_age_gender.loc[['53033032800']].loc[:,'M0-5':'F85-120']

age_gender_dist = KC_age_gender.loc[['53033032800']].loc[:,'M0-5':'F85-120']
freq_dist = FreqDist(age_gender_dist)
prob_dist = MLEProbDist(freq_dist)

print prob_dist.generate()
