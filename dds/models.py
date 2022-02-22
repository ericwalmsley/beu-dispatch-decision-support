from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class DispatchLevel(models.Model):
    #set user based on who is logged in
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    #obs_time options
    noon30 = '1230'
    two30 = '1430'
    four30 = '1630'
    six30 = '1830'
    time_of_observation_choices = [
        (noon30, '12:30'),
        (two30, '14:30'),
        (four30, '16:30'),
        (six30, '18:30'),
    ]
    #Observation time field
    observation_time = models.CharField(
        max_length = 4, #length coordinates to the strings within the obs_time options variables
        choices = time_of_observation_choices,
        default = noon30 #need to figure out auto set method based on current time
        )
    
    #FDRA choices
    coastal_timber = 'COTI'
    sierra_shrub = 'SISH'
    salinas_grass = 'SAGR'
    gabilan_shrub = 'GBSH'
    diablo_grass = 'DIGR'
    fdra_choices = [
        (coastal_timber, 'Coastal Timber'),
        (sierra_shrub, 'Sierra de Salinas Shrub'),
        (salinas_grass, 'Salinas Valley Grass'),
        (gabilan_shrub, 'Gabilan Shrub'),
        (diablo_grass, 'Diablo Grass'),
        ]
    #Fdra field
    Fire_Danger_Rating_Area = models.CharField(
        max_length = 4,
        choices = fdra_choices
        )

    #dispatch level choices
    low = 'L'
    medium = 'M'
    high = 'H'
    very_high = 'V'
    dispatch_level_choices = [
        (low, 'Low'),
        (medium, 'Medium'),
        (high, 'High'),
        (very_high, 'Very High'),
        ]
    
    ###Place holder for automatically set dispatch level###
    #dl_autoSet = models.CharField(....
    
    #dispatch level change field
    Dispatch_Level_Captain_Override = models.CharField(
        max_length = 9,
        choices = dispatch_level_choices,
        #default = automatically set from WIMS data
        )