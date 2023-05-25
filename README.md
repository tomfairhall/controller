# Controller
## Aquairio's System Controller

A Raspberry Pi Powered automated hydroponics controller.

### Functions:
- Measure and log temperature, humidity, lux, pressure.
- View and download logged data over a webserver.
- Remotley update and reboot.

### Todo:
- Add logging period changing function
- Add initialising script
- Update camera controls to modern
- Dynamic tiles
- Cron job integrity (adds job if doesn't exist - related to init script?)
- How to control when there is no System View image?
- Fix paths to not be hardcoded
- Make sure graphs have gaps when nothing is being recorded
- Unify display functions
- Display when the server errors
- Catch measurement error if occours

### Ideas:
- Set up RPI as access point so that wifi switches can connect to it
- Add alarming system (e.g., if light is on longer than expected -> send alarm)