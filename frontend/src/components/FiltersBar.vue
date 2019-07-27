<template>
  <div class="right-block">
    <div class="filter-block">
      <v-select
        v-model="filter.reason"
        :items="absenceReasonOptions"
        menu-props="auto"
        label="Select reason"
        hide-details
        single-line
        @change="setFilter({reason: $event})"
      ></v-select>
      <v-select
        v-model="filter.status"
        :items="absenceStatusOptions"
        menu-props="auto"
        label="Select status"
        hide-details
        @change="setFilter({status: $event})"
        single-line
      ></v-select>
      <v-text-field
        v-model="filter.start_date"
        append-icon="search"
        label="yyyy-mm-dd"
        @change="setFilter({start_date: $event})"
        single-line
        hide-details
      ></v-text-field>
      <v-text-field
        v-model="filter.end_date"
        append-icon="search"
        label="yyyy-mm-dd"
        @change="setFilter({end_date: $event})"
        single-line
        hide-details
      ></v-text-field>
    </div>
    <v-icon @click="clearFilter()">clear</v-icon>
  </div>
</template>

<script>
import * as config from "@/config.js";
import { mapState } from 'vuex';

export default {
  props: {
    setFilter: { type: Function },
  },
  data: () => ({
    absenceReasonOptions: config.absenceReasonOptions,
    absenceStatusOptions: config.absenceStatusOptions
  }),
  
  computed: mapState({
    filter: state => state.absence.filter,
    paginationInfo: state => state.absence.paginationInfo,
  }),

  methods: {
    /*selectedDateFilterValue(val) {
      if (val) {
        const re = /^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$/g;
        const isValid = re.test(val);
        if (isValid) {
          this.createFilter();
        }
      }
    },*/

    clearFilter() {
      this.setFilter({});
    },
  }
};
</script>

<style>
.filter-block {
  display: grid;
  grid-template-columns: 1fr 1fr;
  justify-content: space-between;
  grid-column-gap: 10px;
}
.right-block {
  display: grid;
  grid-template-columns: 9fr 1fr;
}
</style>
