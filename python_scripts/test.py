WEEK_SCHEDULE = [
    [datetime.time( 0, 0), datetime.time( 1, 0)],     # from 00:00 to 01:00
    [datetime.time( 7, 0), datetime.time( 9, 0)],     # from 07:00 to 09:00
    [datetime.time(18, 0), datetime.time(23, 59, 59)] # from 18:00 to 23:59
]
WEEKEND_SCHEDULE = [
    [datetime.time( 0, 0), datetime.time( 2, 0)],
    [datetime.time(10, 0), datetime.time(13, 0)],
    [datetime.time(18, 0), datetime.time(23, 59, 59)]
]

TEMP_HIGH = 19.0
TEMP_LOW  = 17.5

climate_entity = 'climate.central_heating' # set to your thermostat entity
current_temp = hass.states.get(climate_entity).attributes['temperature']

now = datetime.datetime.now().time()
if datetime.datetime.now().date().weekday() < 5:
    current_schedule = WEEK_SCHEDULE
else:
    current_schedule = WEEKEND_SCHEDULE

in_high_time = False
for high_time in current_schedule:
    start = high_time[0]
    end = high_time[1]
    
    if start <= now <= end:        
        in_high_time = True
        break

new_temp = TEMP_HIGH if in_high_time else TEMP_LOW 
if new_temp != current_temp:
    # set the thermostat target temperature.
    hass.services.call('climate', 'set_temperature', {'entity_id': climate_entity, 'temperature': new_temp})

    # also send a notification so that I know that it changed the temperature.
    hass.services.call('script', 'notifications_send', {'title' : 'HA: Changing thermostat', 
        'message': 'Changing temperature to {} (was at {})'.format(new_temp, current_temp)})
    