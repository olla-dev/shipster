# shipster
Track cargo vessels - Kpler Technical Test

## Requirements
### Context

You’ve been hired by a maritime data intelligence company.

They want you to design and develop a webapp visualizing vessel trips and managing vessel positions.
Specs
Base specs

    The web app must have a map to visualize vessel trips.
    The web app must have a table view showing the content of the CSV file.
    Vessel positions should be filterable/sortable by id, date.

We expect you to demonstrate your ui/css skills by delivering a well crafted visual integration.
Advanced specs

You can defend a design if you don’t have the time to implement.

    As a user, I should be able to add / edit / delete positions.
    As a user, I shouldn’t lose my app state when I refresh the page.
    As a user, if I’m using the app and that a peer adds / edits / deletes a position, I should automatically see my peer’s update.

### Exercise

You have a CSV File with an initial list of vessel positions.

    Design an app that matches expectations.
    Defend your design.
    Implement your design.

### Constraints

    Single Page Application built with VueJS and Typescript
    Map visualization built with MapboxGL

### Outputs

Please push your design, explanations and code to a private repository and send us an invit.

Please do not upload your result on a public repository or website.

## Implementation 
* a simple REST API with django (no USER authentication to keep things simple)
* a front-end app in Vue and TypeScript
* Websocket communication using django channels
* Dockerized apps : backend (8080), frontend (3000), db (postgresql: 5432)

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
* GET /api/v1/vessels/{vessel_id}/locations/ : returns the paginated list of locations for a specific vessel 
* POST /api/v1/vessels/{vessel_id}/locations/: adds a location to the vessel
* PUT  /api/v1/vessels/{vessel_id}/locations/{location_id}: update location properties
* DELETE /api/v1/vessels/{vessel_id}/locations/{location_id}: deletes location
* GET /api/v1/vessels/geo/: returns a GeoJson for the latest vessel locations
* GET /api/v1/vessels/csv/: returns a flat paginated list similar to the csv in the specs

#### Performance
The API handles large data. This data is read regularely.
Many techniques can optimize Performance like: 

* Reduce DB queries by optimizing querysets
* Caching: I used django-redis and cached CBVs. It is possible to cache Model objects (relying on django's built in queryset caching)


## Code and repo
In this repo, you will find different work branches (VSS-XX---some-feature). All of them are merged on the main branch along the way (using github PR, for simplicity I kept main as the develop branch).
