# shipster
Track cargo vessels - Kpler Technical Test

## Requirements
Read [here](./REQUIREMENTS.md)

## Implementation 
* a simple REST API with django (no USER authentication to keep things simple)
* a front-end app in Vue and TypeScript
* Websocket communication using django channels
* Dockerized apps : backend (8080), frontend (3000), db (postgresql: 5432), redis (6379)

### Handling Geo data
I'm going to use the GIS extension to handle location data (Points). The REST API will be output paginated vessel locations to the clients.

### Database
In order to handle vessels and their changing geolocations, I will have a basic two models in DB: 
* Vessel (vessel properties, for the moment it only has a vessel_id)
* Location (A geolocation and timestamp)

A vessel has one or many locations

For the sake of simplicity a location belongs to a vessel

### REST API
* GET /api/v1/vessels/ : returns a paginated list of vessels
* GET /api/v1/vessels/{vessel_vessel_id}/locations/ : returns the paginated list of locations for a specific vessel 
* POST /api/v1/vessels/{vessel_vessel_id}/locations/: adds a location to the vessel
* PUT  /api/v1/vessels/{vessel_vessel_id}/locations/{location_id}: update location properties
* DELETE /api/v1/vessels/{vessel_vessel_id}/locations/{location_id}: deletes location
* GET /api/v1/vessels/csv/: returns a flat paginated list similar to the csv in the specs

#### Performance
The API handles large data. This data is read regularely.
Many techniques can optimize Performance like: 

* Reduce DB queries by optimizing querysets
* Caching: I used django-redis and cached CBVs. It is possible to cache Model objects (relying on django's built in queryset caching)

#### UI

I tried to build everything by hand (mapbox and datatables). 
* the map displays all vessels by their latest known position. When clicking a map marker, the journey is displayed (not directional :( just a LineString)
* the datatable lists all locations (paginated). Edit and Delete buttons are contextual to each position. The add button launches a modal.
/!\ I didn't have enough time to make data entry validation better. Sorry :/ Haven't slept alot this week working on the assignment. 

The libraries used are listed on the about page of the app.

## Code and repo
In this repo, you will find different work branches (VSS-XX---some-feature). All of them are merged on the main branch along the way (using github PR, for simplicity I kept main as the develop branch).
