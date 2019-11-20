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
      <v-flex>
        <v-menu
          ref="menu1"
          :close-on-content-click="false"
          v-model="menu1"
          :nudge-right="40"
          :return-value.sync="filter.start_date"
          lazy
          transition="scale-transition"
          offset-y
          full-width
          min-width="390px"
        >
          <v-text-field
            slot="activator"
            v-model="filter.start_date"
            label="Start date"
            prepend-icon="event"
            readonly
          ></v-text-field>
          <v-date-picker
            v-model="filter.start_date"
            @input="$refs.menu1.save(filter.start_date);setFilter({start_date: filter.start_date}) "
          ></v-date-picker>
        </v-menu>
      </v-flex>
      <v-flex>
        <v-menu
          ref="menu2"
          :close-on-content-click="false"
          v-model="menu2"
          :nudge-right="40"
          :return-value.sync="filter.end_date"
          lazy
          transition="scale-transition"
          offset-y
          full-width
          min-width="390px"
        >
          <v-text-field
            slot="activator"
            v-model="filter.end_date"
            label="End date"
            prepend-icon="event"
            readonly
          ></v-text-field>
          <v-date-picker
            v-model="filter.end_date"
            @input="$refs.menu2.save(filter.end_date);setFilter({end_date: filter.end_date}) "
          ></v-date-picker>
        </v-menu>
      </v-flex>
    </div>
    <v-icon @click="clearFilter()">clear</v-icon>
  </div>
</template>

<script>
import * as config from "@/config.js";
import { mapState } from "vuex";

export default {
  props: {
    setFilter: { type: Function }
  },
  data: () => ({
    menu1: false,
    menu2: false,
    absenceReasonOptions: config.absenceReasonOptions,
    absenceStatusOptions: config.absenceStatusOptions
  }),

  computed: mapState({
    filter: state => state.absence.filter,
    paginationInfo: state => state.absence.paginationInfo
  }),

  methods: {
    clearFilter() {
      this.setFilter({});
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
.theme--light.v-input:not(.v-input--is-disabled) input {
  color: #66a4d4;
}
.v-menu__content {
  box-shadow: none !important;
}
.v-picker__title.primary {
  background-color: #003851 !important;
}
</style>
