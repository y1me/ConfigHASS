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
    [datetime.time( 6, 0), datetime.time( 9, 0)],     # from 07:00 to 09:00
    [datetime.time(16, 30), datetime.time(23, 29, 59)] # from 18:00 to 23:59
]

WEEK_NIGHT_SCHEDULE = [

    [datetime.time(00,00), datetime.time(5, 59, 59)],    
    [datetime.time(23, 30), datetime.time(23, 59, 59)] # from 18:00 to 23:59

]

SAT_SCHEDULE = [

    [datetime.time(00,00), datetime.time(00,30)],

    [datetime.time((satmsh),(satmsm)), datetime.time((satmfh),(satmfm))],

    [datetime.time((satesh),(satesm)), datetime.time((satefh),(satefm), 59)]

]

SUN_SCHEDULE = [

    [datetime.time(00,00), datetime.time(00,30)],

    [datetime.time((sunmhs),(sunmms)), datetime.time((sunmfh),(sunmfm))],

    [datetime.time((sunehs),(sunems)), datetime.time((sunefh),(sunefm), 59)]

]

# Initially setup target temps from input_numbers

TEMP_HIGH_LIVINGR = temp_heat_livingr

TEMP_HIGH_BATHR   = temp_heat_bathr

TEMP_HIGH_HALL    = temp_heat_hall

TEMP_LOW_LIVINGR  = temp_heat_away

TEMP_LOW_BATHR    = temp_heat_away

TEMP_LOW_HALL     = temp_heat_away

# Create the climate entities

climate_entity  = 'climate.lr_main'    # set to your thermostat entity

climate_entity1 = 'climate.lr_backup'  # set to your thermostat entity

climate_entity2 = 'climate.bathroom'   # set to your thermostat entity

climate_entity3 = 'climate.hall'       # set to your thermostat entity

# if heating_on (ie autumn/winter/spring)

if heating_on == 'on':

    # test output logging

    #hass.services.call('system_log', 'write', {'message': "heating_on == on"})

    if heating_away == 'on':

        # set  preset_mode to away - climate will use the away temp it was initially set to 

        hass.services.call('climate', 'set_preset_mode', {'entity_id': climate_entity,  'preset_mode': 'away'})

        hass.services.call('climate', 'set_preset_mode', {'entity_id': climate_entity1, 'preset_mode': 'away'})

        hass.services.call('climate', 'set_preset_mode', {'entity_id': climate_entity2, 'preset_mode': 'away'})

        hass.services.call('climate', 'set_preset_mode', {'entity_id': climate_entity3, 'preset_mode': 'away'})

        #hass.services.call('system_log', 'write', {'message': "heating_away == on"})

        exit()

    # if climate override is on 

    if climate_override == 'on':

        TEMP_LOW_LIVINGR = temp_heat_livingr

        TEMP_LOW_BATHR   = temp_heat_bathr

        TEMP_LOW_BATHR   = temp_heat_hall

    # get the current temp for each room

    current_lr_temp       = hass.states.get(climate_entity).attributes['temperature']

    current_bathroom_temp = hass.states.get(climate_entity2).attributes['temperature']

    current_hall_temp     = hass.states.get(climate_entity3).attributes['temperature']

    # get current date and time

    now = datetime.datetime.now().time()

    # determine which scedule is appropriate

    if datetime.datetime.now().date().weekday() < 5: # 0 - 4 Mon-Fri 5 Sat 6 Sun

        current_schedule = WEEK_SCHEDULE

    elif datetime.datetime.now().date().weekday() == 5:

        current_schedule = SAT_SCHEDULE

    else:

        current_schedule = SUN_SCHEDULE

    # determine if we want the heating on for this time in the schedule

    in_high_time = False

    for high_time in current_schedule:

        start = high_time[0]

        end = high_time[1]

        

        if start <= now <= end:        

            in_high_time = True

            break

    # override the scheduler if needed

    if climate_override == 'on':

        in_high_time = True

    new_temp_lr = TEMP_HIGH_LIVINGR if in_high_time else TEMP_LOW_LIVINGR 

    if new_temp_lr != current_lr_temp:

        # set the thermostat target temperature/presetmode/hvac mode and turn on.

        hass.services.call('climate', 'turn_on', {'entity_id': climate_entity})

        hass.services.call('climate', 'set_preset_mode', {'entity_id': climate_entity,  'preset_mode': "none"})

        hass.services.call('climate', 'set_hvac_mode', {'entity_id': climate_entity,  'hvac_mode': "heat"})

        hass.services.call('climate', 'set_temperature', {'entity_id': climate_entity,  'temperature': new_temp_lr, 'hvac_mode': "heat"})

        hass.services.call('climate', 'turn_on', {'entity_id': climate_entity1})

        hass.services.call('climate', 'set_preset_mode', {'entity_id': climate_entity1,  'preset_mode': "none"})

        hass.services.call('climate', 'set_hvac_mode', {'entity_id': climate_entity1,  'hvac_mode': "heat"})

        hass.services.call('climate', 'set_temperature', {'entity_id': climate_entity1, 'temperature': new_temp_lr, 'hvac_mode': "heat"})

        # also send a notification so that I know that it changed the temperature.

        hass.services.call('script', 'ariela_send_notification', {'message': 'Changing Livingroom temperature to {} (was at {})'.format(new_temp_lr, current_lr_temp)})    

    new_temp_br = TEMP_HIGH_BATHR if in_high_time else TEMP_LOW_BATHR

    if new_temp_br != current_bathroom_temp:

        # set the thermostat target temperature/presetmode/hvac mode and turn on.

        hass.services.call('climate', 'turn_on', {'entity_id': climate_entity2})

        hass.services.call('climate', 'set_preset_mode', {'entity_id': climate_entity2,  'preset_mode': "none"})

        hass.services.call('climate', 'set_hvac_mode', {'entity_id': climate_entity2,  'hvac_mode': "heat"})

        hass.services.call('climate', 'set_temperature', {'entity_id': climate_entity2, 'temperature': new_temp_br, 'hvac_mode': "heat"})

        # also send a notification so that I know that it changed the temperature.

        hass.services.call('script', 'ariela_send_notification', {'message': 'Changing Bathroom temperature to {} (was at {})'.format(new_temp_br, current_bathroom_temp)})

        

    new_temp_hall = TEMP_HIGH_HALL if in_high_time else TEMP_LOW_HALL

    if new_temp_hall != current_hall_temp:

        # set the thermostat target temperature/presetmode/hvac mode and turn on.

        hass.services.call('climate', 'turn_on', {'entity_id': climate_entity3})

        hass.services.call('climate', 'set_preset_mode', {'entity_id': climate_entity3,  'preset_mode': "none"})

        hass.services.call('climate', 'set_hvac_mode', {'entity_id': climate_entity3,  'hvac_mode': "heat"})

        hass.services.call('climate', 'set_temperature', {'entity_id': climate_entity3, 'temperature': new_temp_hall, 'hvac_mode': "heat"})

        # also send a notification so that I know that it changed the temperature.

        hass.services.call('script', 'ariela_send_notification', {'message': 'Changing Hall temperature to {} (was at {})'.format(new_temp_hall, current_hall_temp)})

else:

    # if summer turn off heating

    hass.services.call('climate', 'turn_off', {'entity_id': climate_entity})

    hass.services.call('climate', 'turn_off', {'entity_id': climate_entity1})

    hass.services.call('climate', 'turn_off', {'entity_id': climate_entity2})

    hass.services.call('climate', 'turn_off', {'entity_id': climate_entity3})

    # test output logging

    #hass.services.call('system_log', 'write', {'message': "heating_on == off"})

