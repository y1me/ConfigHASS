# Import HA Booleans for override/heating away/heating on

# climate override is for when I'm home earlier then expected or am staying up later then expected

climate_override = hass.states.get('input_boolean.climate_override').state

# heating_away is when I'm away at work or just elsewhere

heating_away     = hass.states.get('input_boolean.heat_away').state

# heating_away is when I'm away at work or just elsewhere

heating_night     = hass.states.get('input_boolean.heating_night').state

# heating_on is an override for the whole scheduler - such as in summer it acts to turn it all off

heating_on       = hass.states.get('input_boolean.heating_on').state



temp_heat_salon    = int(float(hass.states.get('input_number.temp_salon').state))

temp_heat_away    = int(float(hass.states.get('input_number.temp_away').state))

temp_heat_night    = int(float(hass.states.get('input_number.temp_night').state))


WEEK_SCHEDULE = [
    [datetime.time( 5, 30), datetime.time( 8, 0)],     # from 07:00 to 09:00
    [datetime.time(16, 0), datetime.time(21, 59, 59)] # from 18:00 to 23:59
]

WEEK_NIGHT_SCHEDULE = [

    [datetime.time(00,00), datetime.time(5, 29, 59)],    
    [datetime.time(23, 00), datetime.time(23, 59, 59)] # from 18:00 to 23:59

]

WEEKEND_SCHEDULE = [

    [datetime.time( 7, 0), datetime.time( 21, 59, 59)]     # from 07:00 to 09:00
]

WEEKEND_NIGHT_SCHEDULE = [

    [datetime.time(00,00), datetime.time(6, 59, 59)],    
    [datetime.time(22, 00), datetime.time(23, 59, 59)] # from 18:00 to 23:59

]


# Initially setup target temps from input_numbers

TEMP_HEAT_SALON = temp_heat_salon

TEMP_HEAT_NIGHT = temp_heat_night

TEMP_HEAT_AWAY = temp_heat_away

# Create the climate entities

climate_entity  = 'climate.salon'    # set to your thermostat entity

# if heating_on (ie autumn/winter/spring)

if heating_on == 'on':

    # test output logging

    #hass.services.call('system_log', 'write', {'message': "heating_on == on"})

    #if heating_away == 'on':

        # set  preset_mode to away - climate will use the away temp it was initially set to 

        #hass.services.call('climate', 'set_preset_mode', {'entity_id': climate_entity,  'preset_mode': 'away'})

        #hass.services.call('system_log', 'write', {'message': "heating_away == on"})

        #exit()

    # if climate override is on 

    #if climate_override == 'on':

        #TEMP_LOW_LIVINGR = temp_heat_livingr

        #TEMP_LOW_BATHR   = temp_heat_bathr

        #TEMP_LOW_BATHR   = temp_heat_hall

    # get the current temp for each room

    current_salon_temp = hass.states.get(climate_entity).attributes['temperature']

    # get current date and time

    now = datetime.datetime.now().time()

    # determine which scedule is appropriate

    if datetime.datetime.now().date().weekday() < 5: # 0 - 4 Mon-Fri 5 Sat 6 Sun

        current_schedule = WEEK_SCHEDULE
        current_schedule_night = WEEK_NIGHT_SCHEDULE

    #elif datetime.datetime.now().date().weekday() == 5:

        #current_schedule = SAT_SCHEDULE

    else:

        current_schedule = WEEKEND_SCHEDULE
        current_schedule_night = WEEKEND_NIGHT_SCHEDULE

    # determine if we want the heating on for this time in the schedule

    new_temp_salon = TEMP_HEAT_AWAY    

    if climate_override == 'on':
        new_temp_salon = TEMP_HEAT_SALON
    else :
        for high_time in current_schedule:

            start = high_time[0]

            end = high_time[1]

            if start <= now <= end:        

                new_temp_salon = TEMP_HEAT_SALON

                break

    for high_time in current_schedule_night:

        start = high_time[0]

        end = high_time[1]

        if start <= now <= end:        

            new_temp_salon = TEMP_HEAT_NIGHT

            break

    # override the scheduler if needed

    #if climate_override == 'on':

        #in_high_time = True

    if new_temp_salon != current_salon_temp: 

        logger.info("Hello Set salon temp to %s", new_temp_salon)
        # set the thermostat target temperature/presetmode/hvac mode and turn on.

        hass.services.call('climate', 'turn_on', {'entity_id': climate_entity})

        #hass.services.call('climate', 'set_preset_mode', {'entity_id': climate_entity,  'preset_mode': "none"})

        #hass.services.call('climate', 'set_hvac_mode', {'entity_id': climate_entity,  'hvac_mode': "heat"})

        hass.services.call('climate', 'set_temperature', {'entity_id': climate_entity,  'temperature': new_temp_salon, 'hvac_mode': "heat"})

        #hass.services.call('climate', 'turn_on', {'entity_id': climate_entity1})

        #hass.services.call('climate', 'set_preset_mode', {'entity_id': climate_entity1,  'preset_mode': "none"})

        #hass.services.call('climate', 'set_hvac_mode', {'entity_id': climate_entity1,  'hvac_mode': "heat"})

        #hass.services.call('climate', 'set_temperature', {'entity_id': climate_entity1, 'temperature': new_temp_lr, 'hvac_mode': "heat"})

        # also send a notification so that I know that it changed the temperature.

        #hass.services.call('script', 'ariela_send_notification', {'message': 'Changing Livingroom temperature to {} (was at {})'.format(new_temp_lr, current_lr_temp)})    

else:

    # if summer turn off heating

    hass.services.call('climate', 'turn_off', {'entity_id': climate_entity})

    # test output logging

    #hass.services.call('system_log', 'write', {'message': "heating_on == off"})

