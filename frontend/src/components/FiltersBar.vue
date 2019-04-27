<template>
  <div class="right-block">
    <div class="filter-block">
      <v-select
        v-model="selectedTypeOfFilter"
        :items="typeOfFiltresOptions"
        menu-props="auto"
        label="Select type of filter"
        hide-details
        prepend-icon="map"
        single-line
      ></v-select>
      <v-select
        v-if="selectedTypeOfFilter === 'reason' || selectedTypeOfFilter === 'status'"
        v-model="selectedFilter"
        :items="getCurrentOptons()"
        menu-props="auto"
        label="Select filter"
        hide-details
        prepend-icon="map"
        single-line
      ></v-select>
      <v-text-field
        v-if="selectedTypeOfFilter === 'start_date' || selectedTypeOfFilter === 'end_date'"
        v-model="selectedDateFilterValue"
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
  },
  data: () => ({
    selectedDateFilterValue: "",
    selectedTypeOfFilter: "",
    selectedFilter: "",
    absenceReasonOptions: config.absenceReasonOptions,
    typeOfFiltresOptions: config.typeOfFiltresOptions,
    absenceStatusOptions: config.absenceStatusOptions
  }),

  watch: {
    selectedFilter(val) {
      console.log(this, 'this')
      if (val) {
        this.getAbsences({ type: this.selectedTypeOfFilter, value: val });
      }
    },
    selectedDateFilterValue(val) {
      if (val) {
        const re = /^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$/g;
        const isValid = re.test(val);
        if (isValid) {
          this.getAbsences({ type: this.selectedTypeOfFilter, value: val });
        }
      }
    }
  },

  methods: {
    clearFilter() {
      this.selectedDateFilterValue = "";
      this.selectedTypeOfFilter = "";
      this.selectedFilter = "";
      this.getAbsences();
    },
    getCurrentOptons() {
      const currentSelections = this.selectedTypeOfFilter;
      let answer = [];
      switch (currentSelections) {
        case "reason":
          answer = this.absenceReasonOptions;
          break;
        case "status":
          answer = this.absenceStatusOptions;
          break;
      }
      return answer;
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
