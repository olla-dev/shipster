import {
  Module,
  VuexModule,
  MutationAction,
  getModule,
  Action,
  Mutation,
} from 'vuex-module-decorators'
import { notify } from "@kyvg/vue3-notification";
import { CsvData, CsvRow, CsvRowGeo, QueryFilter } from '@/utils/types/index'
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

    this.fetchCsv({ page: this.currentPage, filter: '' });
  }

  @MutationAction({ mutate: ['data', 'currentPage'] })
  async fetchCsv(p: QueryFilter) {
    const data = await vesselApi.fetchCsv(p.page, p.filter);

    return {
      data: data,
      currentPage: p.page
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