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