import { httpClient } from './client'
import { CsvData, Vessel } from '../utils/types'

class VesselApi {
    /**
     * Fetches all vessels and their latest locations from API. 
     * @returns 
     */
    async fetchVessels(): Promise<Vessel[]> {
        return await httpClient.get('vessels/');
    }

    async getVessel(vessel_id: number): Promise<Vessel> {
        return await httpClient.get(`vessels/${vessel_id}/`);
    }


    /**
     * Fetches all vessels in the same original csv format. 
     * @returns 
     */
    async fetchCsv(): Promise<CsvData> {
        return await httpClient.get('vessels/csv');
    }
}

export const vesselApi = new VesselApi();