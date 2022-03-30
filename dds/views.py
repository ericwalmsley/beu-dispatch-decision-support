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

    #print('Payload delivery time: ', str(end-start))

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
    #--Gab Shrub--
    pi_times = [] #pinnacles
    he_times = [] #hernandez
    pa_times = [] #parkfield
    #--Diablo grass
    ho_times = [] #hollister
    sr_times = [] #santa rita
    pr_times = [] #panoche road

    #get times from all stations for the ful models we're interested in
    #for each row
    for times in wims_od['nfdrs']['row']:
        #Coastal Timber
        #if sta = as and fuel model = x
        if times['sta_nm'] == 'ARROYO_SECO' and times['msgc'] == '16X4A':
            #append time to as_times
            as_times.append(times['nfdr_tm'])
        #if sta = bs and fuel model = x
        if times['sta_nm'] == 'BIG SUR' and times['msgc'] == '16X4A':
            #append time to bs_times
            bs_times.append(times['nfdr_tm'])
        #Sds Shrub fdra
        #if sta = hastings, and fuel model = z
        if times['sta_nm'] == 'HASTINGS' and times['msgc'] == '16Z3A':
            #append time to as_times
            ha_times.append(times['nfdr_tm'])
        #if sta = hl and fuel model = z
        if times['sta_nm'] == 'HUNTER LIGGET' and times['msgc'] == '16Z3A':
            #append time to bs_times
            hl_times.append(times['nfdr_tm'])
        #SV grass
        # if sta = br and fm =y
        if times['sta_nm'] == 'BRADLEY' and times['msgc'] == '16Y2A':
            #append time to br_times
            br_times.append(times['nfdr_tm'])
        #if sta = pa and fuel model = y
        if times['sta_nm'] == 'PARKFIELD' and times['msgc'] == '16Y2A':
            #append time to pa_times
            pa_times.append(times['nfdr_tm'])
        #Gab Shrub
        #if sta = he and fm = v
        if times['sta_nm'] == 'HERNANDEZ' and times['msgc'] == '16V3A':
            #append time to as_times
            he_times.append(times['nfdr_tm'])
        #if sta = pi and fuel model = v
        if times['sta_nm'] == 'PINNACLES' and times['msgc'] == '16V2A':
            #append time to bs_times
            pi_times.append(times['nfdr_tm'])
        #Diab Grass
        #if sta = ho and fm = y
        if times['sta_nm'] == 'HOLLISTER' and times['msgc'] == '16Y2A':
            #append time to as_times
            ho_times.append(times['nfdr_tm'])
        #if sta = sr and fuel model = y
        if times['sta_nm'] == 'SANTA RITA' and times['msgc'] == '16Y2A':
            #append time to bs_times
            sr_times.append(times['nfdr_tm'])
        #if sta = pr and fm = y
        if times['sta_nm'] == 'PANOCHE ROAD' and times['msgc'] == '16Y1A':
            #append time to as_times
            pr_times.append(times['nfdr_tm'])

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
            else: #if one station has more times than another
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
        coti_ics_dict = {} #empty dict for storing ignition compontents
        #for each row in wims data
        for ic in wims_od['nfdrs']['row']:
            #find most recent observation time
            if ic['nfdr_tm'] == coti_most_recent_obs_hour:
                #append most recent obs time's IC to dict
                if ic['sta_nm'] == 'ARROYO_SECO' and ic['msgc'] == '16X4A':
                    coti_ics_dict['Arroyo Seco IC'] = float(ic['ic'])
                if ic['sta_nm'] == 'BIG SUR' and ic['msgc'] == '16X4A':
                    coti_ics_dict['Big Sur IC'] = float(ic['ic'])
    else:
        coti_data_unavailable = True

    if sds_most_recent_obs_hour != 'Station(s) have no NFDRS index data available today.':
        sds_ics_dict = {}        
        #for each row in wims data
        for ic in wims_od['nfdrs']['row']:
            #find most recent observation time
            if ic['nfdr_tm'] == sds_most_recent_obs_hour:
                #append most recent obs time's IC to dict
                if ic['sta_nm'] == 'HUNTER LIGGET' and ic['msgc'] == '16Z3A':
                    sds_ics_dict['Hunter Ligget IC'] = float(ic['ic'])
                if ic['sta_nm'] == 'HASTINGS' and ic['msgc'] == '16Z3A':
                    sds_ics_dict['Hastings IC'] = float(ic['ic'])
    else:
        sds_data_unavailable = True

    if svg_most_recent_obs_hour != 'Station(s) have no NFDRS index data available today.':
        svg_ics_dict = {}
        #for each row in wims data
        for ic in wims_od['nfdrs']['row']:
            #find most recent observation time
            if ic['nfdr_tm'] == svg_most_recent_obs_hour:
                #append most recent obs time's IC to dict
                if ic['sta_nm'] == 'BRADLEY' and ic['msgc'] == '16Y2A':
                    svg_ics_dict['Bradley IC'] = float(ic['ic'])
                if ic['sta_nm'] == 'PARKFIELD' and ic['msgc'] == '16Y2A':
                    svg_ics_dict['Parkfield IC'] = float(ic['ic'])
    else:
        svg_data_unavailable = True

    if gsh_most_recent_obs_hour != 'Station(s) have no NFDRS index data available today.':
        #for each row in wims data
        gsh_ics_dict = {}  
        for ic in wims_od['nfdrs']['row']:
            #find most recent observation time
            if ic['nfdr_tm'] == gsh_most_recent_obs_hour:
                #append most recent obs time's IC to dict
                if ic['sta_nm'] == 'HERNANDEZ' and ic['msgc'] == '16V3A':
                    gsh_ics_dict['Hernandez IC'] = float(ic['ic'])
                if ic['sta_nm'] == 'PARKFIELD' and ic['msgc'] == '16V2A': #note that 2 and 3 are different
                    gsh_ics_dict['Parkfield IC'] = float(ic['ic'])
                if ic['sta_nm'] == 'PINNACLES' and ic['msgc'] == '16V2A':
                    gsh_ics_dict['Pinnacles IC'] = float(ic['ic'])
    else:
        gsh_data_unavailable = True

    if dgr_most_recent_obs_hour != 'Station(s) have no NFDRS index data available today.':
        dgr_ics_dict = {}
        for ic in wims_od['nfdrs']['row']:
            #find most recent observation time
            if ic['nfdr_tm'] == dgr_most_recent_obs_hour:
                #append most recent obs time's IC to dict
                if ic['sta_nm'] == 'HOLLISTER' and ic['msgc'] == '16Y2A':
                    dgr_ics_dict['Hollister IC'] = float(ic['ic'])
                if ic['sta_nm'] == 'SANTA RITA' and ic['msgc'] == '16Y2A': #note that 2 and 3 are different
                    dgr_ics_dict['Santa Rita IC'] = float(ic['ic'])
                if ic['sta_nm'] == 'PANOCHE ROAD' and ic['msgc'] == '16Y1A':
                    dgr_ics_dict['Panoche Road IC'] = float(ic['ic'])
    else:
        dgr_data_unavailable = True

    if coti_data_unavailable == False:
        #print('-----Coastal Timber-----')
        #print('Most recently obs time:', coti_most_recent_obs_hour)
        #print('Ignition components:')
        #print(coti_ics_dict)
        #calculate average
        coti_ic = round(sum(coti_ics_dict.values())/len(coti_ics_dict.values()), 2)
        #print('Coastal Timber Ignition Component: ' + str(coti_ic))
        #set Coastal Timber DL
        if coti_ic < 8:
            coti_dl = 'Low'
        elif coti_ic < 23:
            coti_dl = 'Medium'
        elif coti_ic < 68:
            coti_dl = 'High'
        else:
            coti_dl = 'Unprecedented'    
        #print('Coastal Timber Dispatch Level: ' + coti_dl)
    else:
        #print('-----Coastal Timber-----')
        print(coti_most_recent_obs_hour)

    if sds_data_unavailable == False:
        #print('-----Sierra De Salinas Shrub-----')
        #print('Most recently obs time:', sds_most_recent_obs_hour)
        #print('Ignition components: ' )
        #print(sds_ics_dict)
        #calculate average
        sds_ic = round(sum(sds_ics_dict.values())/len(sds_ics_dict.values()), 2)
        #print('Sierra De Salinas Ignition Component: ' + str(sds_ic))
        #set Coastal Timber DL
        if sds_ic < 9:
            sds_dl = 'Low'
        elif sds_ic < 48:
            sds_dl = 'Medium'
        elif sds_ic < 91:
            sds_dl = 'High'
        else:
            sds_dl = 'Unprecedented'    
        #print('Sierra De Salinas Dispatch Level: ' + coti_dl)
    else:
        #print('-----Sierra de Salinas Shrub-----')
        print(sds_most_recent_obs_hour)

    if svg_data_unavailable == False:
        #print('-----Salinas Valley Grass-----')
        #print('Most recently obs time:', svg_most_recent_obs_hour)
        #print('Ignition components: ')
        #print(svg_ics_dict)
        #calculate average
        svg_ic = round(sum(svg_ics_dict.values())/len(svg_ics_dict.values()), 2)
        #print('Salinas Valley Grass Component: ' + str(svg_ic))
        #set Coastal Timber DL
        if svg_ic < 10:
            svg_dl = 'Low'
        elif svg_ic < 38:
            svg_dl = 'Medium'
        elif svg_ic < 76:
            svg_dl = 'High'
        else:
            svg_dl = 'Unprecedented'    
        #print('Salinas Valley Grass Dispatch Level: ' + svg_dl)
    else:
        #print('-----Salinas Valley Grass-----')
        print(svg_most_recent_obs_hour)

    if gsh_data_unavailable == False:
        #print('-----Gabilan Shrub-----')
        #print('Most recently obs time:', gsh_most_recent_obs_hour)
        #print('Ignition components:')
        #print(gsh_ics_dict)
        #calculate average
        gsh_ic = round(sum(gsh_ics_dict.values())/len(gsh_ics_dict.values()), 2)
        #print('Gabilan Shrub Ignition Component: ' + str(gsh_ic))
        #set gab shrub dl
        if gsh_ic < 8:
            gsh_dl = 'Low'
        elif gsh_ic < 33:
            gsh_dl = 'Medium'
        elif gsh_ic < 71:
            gsh_dl = 'High'
        else:
            gsh_dl = 'Unprecedented'
        #print('Gabilan Shrub Dispatch Level: ' + gsh_dl)
    else:
        #print('-----Gabilan Shrub-----')
        print(gsh_most_recent_obs_hour)

    if dgr_data_unavailable == False:
        #print('-----Diablo Grass-----')
        #print('Most recently obs time:', dgr_most_recent_obs_hour)
        #print('Ignition components:')
        #print(dgr_ics_dict)
        #calculate average
        dgr_ic = round(sum(dgr_ics_dict.values())/len(dgr_ics_dict.values()), 2)
        #print('Diablo Grass Ignition Component: ' + str(dgr_ic))
        #set gab shrub dl
        if dgr_ic < 9:
            dgr_dl = 'Low'
        elif dgr_ic < 37:
            dgr_dl = 'Medium'
        elif dgr_ic < 73:
            dgr_dl = 'High'
        else:
            dgr_dl = 'Unprecedented'
        #print('Diablo Grass Dispatch Level: ' + gsh_dl)
    else:
        #print('-----Diablo Grass-----')
        print(dgr_most_recent_obs_hour)

    end_final = datetime.today()

    #print('Payload + data calculation: ', str(end_final-start))

    #print('Payload + data calculation: ', str(end_final-start))
    return render(request, 'dds/base.html', 
    {
    'coti_most_recent_obs_hour':coti_most_recent_obs_hour,
    'coti_ics_dict': coti_ics_dict,
    'coti_ic': coti_ic,
    'coti_dl': coti_dl,
    'sds_most_recent_obs_hour': sds_most_recent_obs_hour,
    'sds_ics_dict': sds_ics_dict,
    'sds_ic': sds_ic,
    'sds_dl': sds_dl,
    'svg_most_recent_obs_hour':svg_most_recent_obs_hour,
    'svg_ics_dict': svg_ics_dict,
    'svg_ic': svg_ic,
    'svg_dl': svg_dl,
    'gsh_most_recent_obs_hour': gsh_most_recent_obs_hour,
    'gsh_ics_dict': gsh_ics_dict,
    'gsh_ic': gsh_ic,
    'gsh_dl': gsh_dl,
    'dgr_most_recent_obs_hour': dgr_most_recent_obs_hour,
    'dgr_ics_dict': dgr_ics_dict,
    'dgr_ic': dgr_ic,
    'dgr_dl': dgr_dl,
    })