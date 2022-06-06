from django.shortcuts import render
from requests import get
from xmltodict import parse
from datetime import datetime

# Create your views here.

def base_map(request):

    start = datetime.today()

    #wims api - coastal timber
    url = "https://famprod.nwcg.gov/wims/xsql/nfdrs.xsql?stn=&sig=beu2&user=ewalmsley&type=N&start=&end=&time=&priority=&fmodel=&sort=&ndays="

    #get the data
    try:
        response = get(url, timeout = 20)
        wims_od = parse(response.content)
        end = datetime.today()
    #error handler
    except ConnectionError as error:
        print("The WIMS server may currently be down. Please try again later.")

    ## Get available times from both stations
    #create list of times for each station
    #--Coastal Timber--
    as_times = []
    bs_times=[] #Arroyo Seco
    #bs_times = [] #Big Sur
    #--SdS Shrub--
    ha_times = [] #hastings
    hl_times = [] #hunter ligget
    #--Sv Grass-- fdra includes parkfield
    br_times = [] #bradley
    pa_times = [] #parkfield
    #--Gab Shrub--
    pi_times = [] #pinnacles
    he_times = [] #hernandez
    #parkfield times already checked above
    #--Diablo grass
    ho_times = [] #hollister
    sr_times = [] #santa rita
    pr_times = [] #panoche road

    #get times from all stations for the ful models we're interested in
    #for each row
    for times in wims_od['nfdrs']['row']:
        #Coastal Timber
        #if sta = as and fuel model = x
        if times['sta_nm'] == 'ARROYO_SECO' and times['msgc'] == '16W4A':
            #append time to as_times
            as_times.append(times['nfdr_tm'])
        #if sta = bs and fuel model = x
        if times['sta_nm'] == 'BIG SUR' and times['msgc'] == '16W4A':
            #append time to bs_times
            bs_times.append(times['nfdr_tm'])
            
        #Sds Shrub fdra
        #if sta = hastings, and fuel model = z
        if times['sta_nm'] == 'HASTINGS' and times['msgc'] == '16V3A':
            #append time to as_times
            ha_times.append(times['nfdr_tm'])
        #if sta = hl and fuel model = z
        if times['sta_nm'] == 'HUNTER LIGGET' and times['msgc'] == '16V3A':
            #append time to bs_times
            hl_times.append(times['nfdr_tm'])
            
        #SV grass
        # if sta = br and fm =y
        if times['sta_nm'] == 'BRADLEY' and times['msgc'] == '16X2A':
            #append time to br_times
            br_times.append(times['nfdr_tm'])
        #if sta = pa and fuel model = y
        if times['sta_nm'] == 'PARKFIELD' and times['msgc'] == '16X2A':
            #append time to pa_times
            pa_times.append(times['nfdr_tm'])
            
        #Gab Shrub
        #if sta = he and fm = v
        if times['sta_nm'] == 'HERNANDEZ' and times['msgc'] == '16X3A':
            #append time to as_times
            he_times.append(times['nfdr_tm'])
        #if sta = pi and fuel model = v
        if times['sta_nm'] == 'PINNACLES' and times['msgc'] == '16X2A':
            #append time to bs_times
            pi_times.append(times['nfdr_tm'])
        #Parkfield already addressed above
        
        #Diab Grass
        #if sta = ho and fm = y
        if times['sta_nm'] == 'HOLLISTER' and times['msgc'] == '16Z2A':
            #append time to as_times
            ho_times.append(times['nfdr_tm'])
        #if sta = sr and fuel model = y
        if times['sta_nm'] == 'SANTA RITA' and times['msgc'] == '16Z2A':
            #append time to bs_times
            sr_times.append(times['nfdr_tm'])
        #if sta = pr and fm = y
        if times['sta_nm'] == 'PANOCHE ROAD' and times['msgc'] == '16Z1A':
            #append time to as_times
            pr_times.append(times['nfdr_tm'])

    #convert to integers and sort so we can calculate dispatch level for the entire day
    def ints_and_sort(list):
        list = [int(i) for i in list]
        list.sort()
        return list

    as_times = ints_and_sort(as_times); bs_times = ints_and_sort(bs_times); ha_times = ints_and_sort(ha_times)
    hl_times = ints_and_sort(hl_times); br_times = ints_and_sort(br_times); pa_times = ints_and_sort(pa_times)
    pi_times = ints_and_sort(pi_times); he_times = ints_and_sort(he_times); ho_times = ints_and_sort(ho_times)
    sr_times = ints_and_sort(sr_times); pr_times = ints_and_sort(pr_times)

    ## Compare times to determine most recent observation
    #if lists are the same, using sets because the order is inconsistent
    def get_most_recent_obs_time(station_times_list, station2_times_list, station3_times_list = None):
        #two lists
        if station3_times_list == None:
            if set(station_times_list) == set(station2_times_list): #Checks if times at stations are the same
                times = [int(i) for i in station_times_list] #convert list items to int
                try:
                    most_recent_obs_time = str(max(times)) #get most recent time
                except ValueError as error:
                    #handle the no data currently available
                    most_recent_obs_time = 'Station(s) have no NFDRS index data available today.'
                return most_recent_obs_time
            else: #if one station has more times than another
                #Get the values that are in both lists and put into new list
                times_at_all_stations = [v for v in station_times_list and station2_times_list if v in station_times_list and v in station2_times_list]
                #convert list items to integers
                times_at_all_stations = [int(i) for i in times_at_all_stations]
                #max list = current obs time
                try:
                    most_recent_obs_time = str(max(times_at_all_stations)) #get most recent time
                except ValueError as error:
                    #handle the no data currently available
                    most_recent_obs_time = 'Station(s) have no NFDRS index data available today.'
                return most_recent_obs_time
        #more than two lists
        else:
            if set(station_times_list) == set(station2_times_list) == set(station3_times_list): #check if times are the same
                times = [int(i) for i in station_times_list] #convert to int
                most_recent_obs_time = str(max(times)) #get most recent
                try:
                    most_recent_obs_time = str(max(times)) #get most recent time
                except ValueError as error:
                    #handle the no data currently available
                    most_recent_obs_time = 'Station(s) have no NFDRS index data available today.'
                return most_recent_obs_time
            else: #if one station has more or less times than another
                #get values that are in all stations, put into another list
                times_at_all_stations = [v for v in station_times_list and station2_times_list and station3_times_list if v in station_times_list and v in station2_times_list and v in station3_times_list]
                #convert list items to integers
                times_at_all_stations = [int(i) for i in times_at_all_stations]
                #max list = current obs time
                try:
                    most_recent_obs_time = str(max(times_at_all_stations)) #get most recent time
                except ValueError as error:
                    #handle the no data currently available
                    most_recent_obs_time = 'Station(s) have no NFDRS index data available today.'
                return most_recent_obs_time

    coti_most_recent_obs_hour = get_most_recent_obs_time(bs_times, as_times) #coastal timber most recent hour
    sds_most_recent_obs_hour = get_most_recent_obs_time(ha_times, hl_times) #Sierra De Salinas most recent hour
    svg_most_recent_obs_hour = get_most_recent_obs_time(br_times, pa_times) #Salinas grass most recent hour
    gsh_most_recent_obs_hour = get_most_recent_obs_time(pi_times, pa_times, he_times) #Gab Sh most recent hour
    dgr_most_recent_obs_hour = get_most_recent_obs_time(ho_times, pr_times, sr_times) #Diab gr most recent hour


    #catch variable for times when data is unavailable
    coti_data_unavailable = False
    sds_data_unavailable = False
    svg_data_unavailable = False
    gsh_data_unavailable = False
    dgr_data_unavailable = False

    if coti_most_recent_obs_hour != 'Station(s) have no NFDRS index data available today.':
        coti_bis_dict = {} #empty dict for storing ignition compontents
        #for each row in wims data
        for bi in wims_od['nfdrs']['row']:
            #find most recent observation time
            if bi['nfdr_tm'] == coti_most_recent_obs_hour:
                #append most recent obs time's IC to dict
                if bi['sta_nm'] == 'ARROYO_SECO' and bi['msgc'] == '16W4A':
                    coti_bis_dict['Arroyo Seco BI'] = float(bi['bi'])
                if bi['sta_nm'] == 'BIG SUR' and bi['msgc'] == '16W4A':
                    coti_bis_dict['Big Sur BI'] = float(bi['bi'])
    else:
        coti_data_unavailable = True

    if sds_most_recent_obs_hour != 'Station(s) have no NFDRS index data available today.':
        sds_bis_dict = {}        
        #for each row in wims data
        for bi in wims_od['nfdrs']['row']:
            #find most recent observation time
            if bi['nfdr_tm'] == sds_most_recent_obs_hour:
                #append most recent obs time's IC to dict
                if bi['sta_nm'] == 'HUNTER LIGGET' and bi['msgc'] == '16V3A':
                    sds_bis_dict['Hunter Ligget BI'] = float(bi['bi'])
                if bi['sta_nm'] == 'HASTINGS' and bi['msgc'] == '16V3A':
                    sds_bis_dict['Hastings BI'] = float(bi['bi'])
    else:
        sds_data_unavailable = True

    if svg_most_recent_obs_hour != 'Station(s) have no NFDRS index data available today.':
        svg_bis_dict = {}
        #for each row in wims data
        for bi in wims_od['nfdrs']['row']:
            #find most recent observation time
            if bi['nfdr_tm'] == svg_most_recent_obs_hour:
                #append most recent obs time's IC to dict
                if bi['sta_nm'] == 'BRADLEY' and bi['msgc'] == '16X2A':
                    svg_bis_dict['Bradley BI'] = float(bi['bi'])
                if bi['sta_nm'] == 'PARKFIELD' and bi['msgc'] == '16X2A':
                    svg_bis_dict['Parkfield BI'] = float(bi['bi'])
    else:
        svg_data_unavailable = True

    if gsh_most_recent_obs_hour != 'Station(s) have no NFDRS index data available today.':
        #for each row in wims data
        gsh_bis_dict = {}  
        for bi in wims_od['nfdrs']['row']:
            #find most recent observation time
            if bi['nfdr_tm'] == gsh_most_recent_obs_hour:
                #append most recent obs time's IC to dict
                if bi['sta_nm'] == 'HERNANDEZ' and bi['msgc'] == '16X3A':
                    gsh_bis_dict['Hernandez BI'] = float(bi['bi'])
                if bi['sta_nm'] == 'PARKFIELD' and bi['msgc'] == '16X2A': #note that 2 and 3 are different
                    gsh_bis_dict['Parkfield BI'] = float(bi['bi'])
                if bi['sta_nm'] == 'PINNACLES' and bi['msgc'] == '16X2A':
                    gsh_bis_dict['Pinnacles BI'] = float(bi['bi'])
    else:
        gsh_data_unavailable = True

    if dgr_most_recent_obs_hour != 'Station(s) have no NFDRS index data available today.':
        dgr_bis_dict = {}
        for bi in wims_od['nfdrs']['row']:
            #find most recent observation time
            if bi['nfdr_tm'] == dgr_most_recent_obs_hour:
                #append most recent obs time's IC to dict
                if bi['sta_nm'] == 'HOLLISTER' and bi['msgc'] == '16Z2A':
                    dgr_bis_dict['Hollister BI'] = float(bi['bi'])
                if bi['sta_nm'] == 'SANTA RITA' and bi['msgc'] == '16Z2A': #note that 2 and 3 are different
                    dgr_bis_dict['Santa Rita BI'] = float(bi['bi'])
                if bi['sta_nm'] == 'PANOCHE ROAD' and bi['msgc'] == '16Z1A':
                    dgr_bis_dict['Panoche Road BI'] = float(bi['bi'])
    else:
        dgr_data_unavailable = True

    if coti_data_unavailable == False:
        #calculate average
        coti_bi = round(sum(coti_bis_dict.values())/len(coti_bis_dict.values()), 2)
        #set Coastal Timber DL
        if coti_bi <= 8:
            coti_dl = 'Low'
        elif coti_bi <= 24:
            coti_dl = 'Medium'
        elif coti_bi <= 56:
            coti_dl = 'High'
        else:
            coti_dl = 'Unprecedented'
    else:
        coti_dl = "--"

    if sds_data_unavailable == False:
        #calculate average
        sds_bi = round(sum(sds_bis_dict.values())/len(sds_bis_dict.values()), 2)
        #set DL
        if sds_bi <= 8:
            sds_dl = 'Low'
        elif sds_bi <= 30:
            sds_dl = 'Medium'
        elif sds_bi <= 83:
            sds_dl = 'High'
        else:
            sds_dl = 'Unprecedented'
    else:
        sds_dl = "--"

    if svg_data_unavailable == False:
        #calculate average
        svg_bi = round(sum(svg_bis_dict.values())/len(svg_bis_dict.values()), 2)
        #set DL
        if svg_bi <= 53:
            svg_dl = 'Low'
        elif svg_bi <= 126:
            svg_dl = 'Medium'
        elif svg_bi <= 245:
            svg_dl = 'High'
        else:
            svg_dl = 'Unprecedented'
    else:
        svg_dl = "--"

    if gsh_data_unavailable == False:
        #calculate average
        gsh_bi = round(sum(gsh_bis_dict.values())/len(gsh_bis_dict.values()), 2)
        #set gab shrub dl
        if gsh_bi <= 60:
            gsh_dl = 'Low'
        elif gsh_bi <= 160:
            gsh_dl = 'Medium'
        elif gsh_bi <= 258:
            gsh_dl = 'High'
        else:
            gsh_dl = 'Unprecedented'
    else:
        print(gsh_most_recent_obs_hour)

    if dgr_data_unavailable == False:
        #calculate average
        dgr_bi = round(sum(dgr_bis_dict.values())/len(dgr_bis_dict.values()), 2)
        #set gab shrub dl
        if dgr_bi <= 58:
            dgr_dl = 'Low'
        elif dgr_bi <= 90:
            dgr_dl = 'Medium'
        elif dgr_bi <= 152:
            dgr_dl = 'High'
        else:
            gsh_dl = 'Unprecedented'
    else:
        print(dgr_most_recent_obs_hour)

    end_final = datetime.today()
    dispatchLevelsCalculated = True
    #print('Payload + data calculation: ', str(end_final-start))

    #print('Payload + data calculation: ', str(end_final-start))
    return render(request, 'dds/base.html', 
            {
            'coti_most_recent_obs_hour':coti_most_recent_obs_hour,
            'coti_bis_dict': coti_bis_dict,
            'coti_bi': coti_bi,
            'coti_dl': coti_dl,
            'sds_most_recent_obs_hour': sds_most_recent_obs_hour,
            'sds_bis_dict': sds_bis_dict,
            'sds_bi': sds_bi,
            'sds_dl': sds_dl,
            'svg_most_recent_obs_hour':svg_most_recent_obs_hour,
            'svg_bis_dict': svg_bis_dict,
            'svg_bi': svg_bi,
            'svg_dl': svg_dl,
            'gsh_most_recent_obs_hour': gsh_most_recent_obs_hour,
            'gsh_bis_dict': gsh_bis_dict,
            'gsh_bi': gsh_bi,
            'gsh_dl': gsh_dl,
            'dgr_most_recent_obs_hour': dgr_most_recent_obs_hour,
            'dgr_bis_dict': dgr_bis_dict,
            'dgr_bi': dgr_bi,
            'dgr_dl': dgr_dl,
            })