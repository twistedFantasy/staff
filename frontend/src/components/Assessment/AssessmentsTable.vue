<template>
  <div class="assessments-table-container">
    <div class="assessments-table">
      <v-toolbar flat color="white" class="table-header">
        <v-toolbar-title>My assessments</v-toolbar-title>
      </v-toolbar>
      <v-data-table :headers="headers" :items="assessments" class="elevation-2" hide-actions>
        <template slot="items" slot-scope="props">
          <td>{{ props.item.status }}</td>
          <td class="text-xs-left">{{ props.item.start_date }}</td>
          <td class="text-xs-left">{{ props.item.end_date }}</td>
           <td class="text-xs-left">{{ props.item.plan }}</td>
            <td class="text-xs-left">{{ props.item.comments }}</td>
          <td class="text-xs-left">{{ props.item.notes }}</td>
        </template>
      </v-data-table>
    </div>
    <div class="text-xs-center pagination">
      <v-pagination
        v-model="paginationInfo.page"
        :length="paginationInfo.count"
        :total-visible="7"
        circle
      ></v-pagination>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  data: () => ({
    headers: [
      { text: "Name", value: "name" },
      {
        text: "Status",
        align: "left",
        sortable: true,
        value: "status"
      },
      { text: "Start Data", value: "start_date" },
      { text: "End Data", value: "end_date" },
      { text: "Plan", value: "plan" },
      { text: "Comments", value: "comments" },
      { text: "Descriptions", value: "notes" },
    ],
  }),
  computed: mapState({
    assessments: state => state.assessment.allAssessments,
    paginationInfo: state => state.assessment.paginationInfo
  }),

  watch: {
    "paginationInfo.page"() {
      this.getAssessments();
    }
  },

  created() {
    this.getAssessments();
  },

  methods: {
    ...mapActions({
      getAssessments: "assessment/getAssessments",
      setPaginationInfo: "assessment/setPaginationInfo",
    }),

    onSetPagination(paginationInfo) {
      this.setPaginationInfo(paginationInfo);
    },
  }
};

/*
move modal in diff component

*/
</script>

<style>
.icon,
.theme--light.v-datatable thead th.column.sortable.active,
.theme--light.v-datatable thead th.column.sortable.active .v-icon,
.theme--light.v-datatable thead th.column.sortable {
  color: #66a4d4 !important;
}
.primary.custom-btn {
  background: rgba(117, 169, 209, 0.2) !important;
  border-radius: 24px;
  color: #66a4d4 !important;
  font-size: 12px;
}
.theme--light.v-table tbody tr:hover:not(.v-datatable__expand-row) {
  background: rgba(102, 164, 212, 0.5);
  cursor: pointer;
}
.v-datatable.v-table.theme--light {
  background: #003851;
  color: #66a4d4;
  border-radius: 10px;
}
.absence-table-container {
  margin: 20px 40px 100px 40px;
}
.absence-table-container .v-dialog__container {
  width: 100%;
  display: flex !important;
  justify-content: flex-end;
}
.table-header.v-toolbar.elevation-0.theme--light.white {
  background: #003851 !important;
  border-radius: 10px;
  color: #66a4d4 !important;
}
.table-header .v-toolbar__content {
  width: 100%;
  display: grid;
  grid-template-columns: 2fr 8fr;
  justify-content: space-between;
  grid-column-gap: 10px;
  padding: 0;
  margin: 20px 0;
  padding: 0 10px;
}
.filter-block {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  justify-content: space-between;
  grid-column-gap: 15px;
}
.right-block {
  display: grid;
  grid-template-columns: 9fr 1fr;
}
.pagination {
  margin-top: 20px;
}
.theme--light.v-pagination .v-pagination__item,
.v-pagination__navigation,
.absence-table .v-select__slot > label,
.absence-table .theme--light.v-label,
.v-icon.material-icons.theme--light {
  color: #66a4d4 !important;
}
.create-absance {
  background:  rgba(102, 164, 212, 1)!important;
 color: #66a4d4 !important;
}

</style>

