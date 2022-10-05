import { httpClient } from './client'
import { CsvData, CsvRow, CsvRowGeo, Location, Vessel } from '../utils/types'

class VesselApi {
    /**
     * Fetches all vessels and their latest locations from API. 
     * @returns 
     */
    async fetchVessels(): Promise<Vessel[]> {
        return await httpClient.get('vessels/');
    }

    /**
     * Get a Vessel by id
     * @param vessel_id vessel_id
     * @returns 
     */
    async getVessel(vessel_id: number): Promise<Vessel> {
        return await httpClient.get(`vessels/${vessel_id}/`);
    }

    /**
     * Saves a new location
     * @param row : flat location representation
     */
    async saveLocation(csvRow: CsvRowGeo) {
        return await httpClient.post(`vessels/${csvRow.vessel_id}/locations/`, csvRow)
    }

    /**
     * Updates a specific location
     * @param row : flat location representation
     */
    async updateLocation(csvRow: CsvRowGeo) {
        return await httpClient.put(`vessels/${csvRow.vessel_id}/locations/${csvRow.location_id}/`, csvRow)
    }

    /**
     * Deletes a specific location
     * @param row : flat location representation
     */
    async deleteLocation(csvRow: CsvRow) {
        return await httpClient.delete(`vessels/${csvRow.vessel_id}/locations/${csvRow.location_id}/`)
    }


    /**
     * Fetches all vessels in the same original csv format. 
     * @returns 
     */
    async fetchCsv(page = 1, filter = ''): Promise<CsvData> {
        return await httpClient.get(`vessels/csv?page=${page}&filter=${filter}`);
    }
}

export const vesselApi = new VesselApi();