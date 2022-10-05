import {
  Module,
  VuexModule,
  MutationAction,
  getModule,
  Action,
  Mutation,
} from 'vuex-module-decorators'
import { notify } from "@kyvg/vue3-notification";
import { CsvData, CsvRow, CsvRowGeo } from '@/utils/types/index'
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
  currentPage = 1;
  selectedRow: CsvRow = {} as CsvRow;
  filteredRows: CsvRow[] = [];

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

  /**
   * Returns all known vessel ids in the CSV data
   */
  get vesselList() {
    return [...new Set(this.data.results.map(item => item.vessel_id))];
  }

  /**
   * Returns filtered data
   * @param row 
   */
  get filteredLocations() {
    return (filter: string) => {
      this.data.results.filter(
        row => {
          return row.vessel_id.toString().includes(filter)
            || row.received_time_utc.toString().includes(filter)
            || row.latitude.toString().includes(filter)
            || row.longitude.toString().includes(filter)
        }
      )
    };
  }

  @Mutation
  setSelectedRow(row: CsvRow) {
    this.selectedRow = row;
  }

  @Action({ rawError: true })
  async deleteLocation(csvRow: CsvRow) {
    const data = await vesselApi.deleteLocation(csvRow);
    if (data === 204) {
      notify({
        text: "Location deleted!",
        type: 'success',
        duration: 10000,
      });
    }

    this.fetchCsv(this.currentPage);
  }

  @MutationAction({ mutate: ['data', 'currentPage'] })
  async fetchCsv(page = 1) {
    const data = await vesselApi.fetchCsv(page);

    return {
      data: data,
      currentPage: page
    }
  }

  @Action({ rawError: true })
  async updateLocation(row: CsvRowGeo) {
    await vesselApi.updateLocation(row);
  }

  @Action({ rawError: true })
  async saveLocation(row: CsvRowGeo) {
    await vesselApi.saveLocation(row);
  }
}

const csvModule = getModule(CsvModule)
export default csvModule