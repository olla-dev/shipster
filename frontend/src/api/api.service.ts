import { httpClient } from './client'
import { Vessel } from '../utils/types'

class VesselApi {
    /**
     * Fetches all vessels and their latest locations from API. 
     * @returns 
     */
    async fetchVessels(): Promise<Vessel[]> {
        return await httpClient.get('vessels/geo');
    }

    async getVessel(vessel_id: number): Promise<Vessel> {
        return await httpClient.get(`vessels/${vessel_id}/`);
    }
}

export const vesselApi = new VesselApi();