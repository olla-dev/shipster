import {
  Module,
  VuexModule,
  MutationAction,
  getModule
} from 'vuex-module-decorators'
import { CsvData, CsvRow } from '@/utils/types/index'
import { vesselApi } from '@/api/api.service'
import store from './index'

@Module({ dynamic: true, store, name: 'csv' })
class CsvModule extends VuexModule {
  data: CsvData = {
    links: {
      next: '',
      previous: ''
    },
    results: new Array<CsvRow>()
  };

  /**
   * Returns a specific Vessel by its vessel_id
   */
  get row() {
    return (vessel_id: number) => {
      this.data.results.find(
        row => row.vessel_id === vessel_id
      )
    };
  }

  @MutationAction
  async fetchCsv() {
    const data = await vesselApi.fetchCsv();
    return { data }
  }
}

const csvModule = getModule(CsvModule)
export default csvModule