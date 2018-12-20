import datetime
import numpy as np
import numpy.random as ran
import pandas as pd

import pickle
from nltk.probability import FreqDist, MLEProbDist

#pd.set_option('display.expand_frame_repr', False)

print "loading data..."
KC_age_gender = pd.read_pickle('input/KC_CT_age_gender.pickle')
residential_address = pd.read_pickle('input/KC_residential_censustract.pickle')
print "load complete."

#devide to two regions based on census tract code (roughly west of Lake Washington vs east with a few exceptions)
#see map here: https://www2.census.gov/geo/maps/dc10map/tract/st53_wa/c53033_king/DC10CT_C53033_001.pdf
residential_address['CT_CODE'] = residential_address['GEOID'].str[6:9].dropna().astype(int)

residential_address_A = residential_address[residential_address['CT_CODE'] <= 215]
residential_address_B = residential_address[residential_address['CT_CODE'] > 215]
residential_address_RSV = residential_address[(residential_address['CT_CODE'] > 218) & (residential_address['CT_CODE'] < 251)] #Eastside

def get_gender_age(full_address):
    GEOID = full_address['GEOID']
    try:
        age_gender_dist = KC_age_gender.loc[[GEOID]].loc[:,'M0-4':'F85-120']
        age_gender_freq_dist = FreqDist(age_gender_dist)
        age_gender_prob_dist_age_gender = MLEProbDist(age_gender_freq_dist)
        age_gender_random = age_gender_prob_dist_age_gender.generate()
        gender = age_gender_random[0]
        age = age_gender_random[1:]
        return gender, age
    except:
        return np.nan, np.nan

def add_individual(infection_individuals, res_address, diagnosis):
    diagnosis_freq_dist = FreqDist(diagnosis)
    diagnosis_prob_dist = MLEProbDist(diagnosis_freq_dist)
    diagnosis_random = diagnosis_prob_dist.generate()
    new_address = res_address.sample().to_dict('records')[0]
    full_address = new_address['ADDR_FULL'] + '|' + new_address['CTYNAME'] + '|' + new_address['ZIP5']
    gender, age = get_gender_age(new_address)
    infection_individuals = infection_individuals.append({'Date_Inf': current_date, 'Gender': gender, 'Age': age, 'Census_Tract': new_address['GEOID'], 'Address':full_address, 'LON':new_address['LON'], 'LAT':new_address['LAT'], 'Diagnosis': diagnosis_random}, ignore_index=True)
    return infection_individuals

#test_address = residential_address_A.sample().to_dict('records')[0]
#gender, age = get_gender_age(test_address)
#print gender, age
#exit(1)

popA = 500000.0
popB = 500000.0
totalpop = popA + popB
init_infection = 10

sampling_rate = 0.1

nonflu_rate = 0.01

nonflu_diagnosis = {"Parainfluenza": 0.1, "Rhinovirus": 0.25, "Coronavirus":0.25, "Adenovirus":0.25, "Negative": 0.15}

SA = popA - init_infection
IA = init_infection
RA = 0

start_time_B = 30
SB = popB
IB = 0
RB = 0

popRSV = 50000
start_time_RSV = 15
SRSV = popRSV
IRSV = 0
RRSV = 0



#reproductive number
R0 = 1.5
R0RSV = 3
#recover rate
mu = 1.0/3.0
beta = R0 * mu
betaRSV = R0RSV * mu

timesteps = 365 #each time step is one day

current_date = datetime.date(2018, 9, 1)

infection_individuals = pd.DataFrame(columns=['Date_Inf','Gender','Age','Census_Tract', 'Address', 'LON', 'LAT', "Diagnosis"])

#compartmental SIR

for t in xrange(timesteps):
    print "t="+str(t)
    #seed
    if t == start_time_B:
        SB = popB - init_infection
        IB = init_infection

    if t == start_time_RSV:
        SRSV = popRSV - init_infection
        IRSV = init_infection

    irateA = beta * float(IA) / float(popA)
    rrateA = mu
    newinfA = ran.binomial(SA, irateA)
    newrecA = ran.binomial(IA, rrateA)

    irateB = beta * float(IB) / float(popB)
    rrateB = mu
    newinfB = ran.binomial(SB, irateB)
    newrecB = ran.binomial(IB, rrateB)

    irateRSV = betaRSV * float(IRSV) / float(popRSV)
    rrateRSV = mu
    newinfRSV = ran.binomial(SRSV, irateRSV)
    newrecRSV = ran.binomial(IRSV, rrateRSV)

    SA = SA - newinfA
    IA = IA + newinfA - newrecA
    RA = RA + newrecA
    SB = SB - newinfB
    IB = IB + newinfB - newrecB
    RB = RB + newrecB

    SRSV = SRSV - newinfRSV
    IRSV = IRSV + newinfRSV - newrecRSV
    RRSV = RRSV + newrecRSV

    #non-flu
    number_individuals_nonflu = ran.binomial(totalpop, nonflu_rate*sampling_rate)
    number_individuals_newinfA = ran.binomial(newinfA, sampling_rate)
    number_individuals_newinfB = ran.binomial(newinfB, sampling_rate)
    number_individuals_newinfRSV = ran.binomial(newinfRSV, sampling_rate)

    print t, number_individuals_nonflu, number_individuals_newinfA, number_individuals_newinfB, number_individuals_newinfRSV

    #write fake individual records
    for idx in xrange(number_individuals_nonflu):
        infection_individuals = add_individual(infection_individuals, residential_address, nonflu_diagnosis)
    for idx in xrange(number_individuals_newinfA):
        infection_individuals = add_individual(infection_individuals, residential_address_A, {"Influenza": 1})
    for idx in xrange(number_individuals_newinfB):
        infection_individuals = add_individual(infection_individuals, residential_address_B, {"Influenza": 1})
    for idx in xrange(number_individuals_newinfRSV):
        infection_individuals = add_individual(infection_individuals, residential_address_RSV, {"RSV": 1})
    current_date = current_date + datetime.timedelta(days=1)

infection_individuals.to_pickle("output/infection_individuals.pickle")
infection_individuals.to_csv("output/infection_individuals.csv")
