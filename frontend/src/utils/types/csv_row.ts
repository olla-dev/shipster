export type CsvData = {
    links: {
        'next': string;
        'previous': string;
    },
    results: CsvRow[];
}

export type CsvRow = {
    location_id: number,
    vessel_id: number,
    received_time_utc: string;
    latitude: number;
    longitude: number;
}

export type CsvRowGeo = {
    location_id: number,
    vessel_id: number,
    received_time_utc: string,
    point: {
        "type": "Point",
        "coordinates": [number, number]
    }
}

export type QueryFilter = {
    page: number,
    filter: string
}