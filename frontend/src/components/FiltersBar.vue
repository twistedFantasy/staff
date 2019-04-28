<template>
  <div class="right-block">
    <div class="filter-block">
      <v-select
        v-model="selectedReason"
        :items="absenceReasonOptions"
        menu-props="auto"
        label="Select reason"
        hide-details
        single-line
      ></v-select>
      <v-select
        v-model="selectedStatus"
        :items="absenceStatusOptions"
        menu-props="auto"
        label="Select status"
        hide-details
        single-line
      ></v-select>
      <v-text-field
        v-model="selectedStartDate"
        append-icon="search"
        label="yyyy-mm-dd"
        single-line
        hide-details
      ></v-text-field>
      <v-text-field
        v-model="selectedEndDate"
        append-icon="search"
        label="yyyy-mm-dd"
        single-line
        hide-details
      ></v-text-field>
    </div>
    <v-icon @click="clearFilter()">clear</v-icon>
  </div>
</template>

<script>
import * as config from "@/config.js";

export default {
  props: {
    getAbsences: { type: Function },
    setPagination: { type: Function }
  },
  data: () => ({
    selectedReason: "",
    selectedStatus: "",
    selectedStartDate: "",
    selectedEndDate: "",
    absenceReasonOptions: config.absenceReasonOptions,
    absenceStatusOptions: config.absenceStatusOptions
  }),

  watch: {
    selectedReason() {
      this.createFilter();
    },
    selectedStatus() {
      this.createFilter();
    },
    selectedStartDate(val) {
      this.selectedDateFilterValue(val);
    },
    selectedEndDate(val) {
      this.selectedDateFilterValue(val);
    }
  },

  methods: {
    selectedDateFilterValue(val) {
      if (val) {
        const re = /^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$/g;
        const isValid = re.test(val);
        if (isValid) {
          this.createFilter();
        }
      }
    },

    clearFilter() {
      this.selectedReason = "";
      this.selectedStatus = "";
      this.selectedStartDate = "";
      this.selectedEndDate = "";
      this.getAbsences("");
    },

    createFilter() {
      let result = "";
      this.setPagination({page: 1, count: 1});
      if (this.selectedReason) {
        result = result + `reason=${this.selectedReason}&`;
      }
      if (this.selectedStatus) {
        result = result + `status=${this.selectedStatus}&`;
      }
      if (this.selectedStartDate) {
        result = result + `start_date=${this.selectedStartDate}&`;
      }
      if (this.selectedEndDate) {
        result = result + `end_date=${this.selectedEndDate}&`;
      }
      this.getAbsences(result);
    }
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
