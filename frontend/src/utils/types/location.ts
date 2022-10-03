import { Point } from 'geojson'

export interface Location {
    id: number,
    received_time_utc: String,
    point: Point
};