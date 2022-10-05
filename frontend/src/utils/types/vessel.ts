import { Feature, LineString, GeoJsonProperties, Point } from 'geojson'

export type Vessel = {
    vessel_id: number,
    properties: GeoJsonProperties;
    latest_location: Feature<Point>;
    journey: Feature<LineString>;
};
