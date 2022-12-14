import {
  Module,
  VuexModule,
  MutationAction,
  Mutation,
  getModule
} from 'vuex-module-decorators'
import { Vessel } from '@/utils/types/index'
import { vesselApi } from '@/api/api.service'
import store from './index'

@Module({ dynamic: true, store, name: 'vessels' })
class VesselModule extends VuexModule {
  vessels: Vessel[] = [];
  selectedVessel: Vessel | undefined = undefined;

  /**
   * Returns a specific Vessel by its vessel_id
   */
  get vessel() {
    return (vessel_id: number) => {
      this.vessels.find(
        vessel => vessel.vessel_id === vessel_id
      )
    };
  }

  get getSelectedVessel(): Vessel | undefined {
    return this.selectedVessel;
  }

  @Mutation
  setSelectedVessel(vessel_id: number) {
    this.selectedVessel = this.vessels.find(vessel => vessel.vessel_id === vessel_id);
  }

  @MutationAction
  async fetchVessels() {
    const vessels = await vesselApi.fetchVessels();
    return { vessels }
  }
}

const vesselModule = getModule(VesselModule)
export default vesselModule