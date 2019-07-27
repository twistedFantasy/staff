<template>
  <div class="absence-table-container">
    <v-dialog  v-model="dialog" max-width="500px">
      <v-btn slot="activator" color="primary" dark class="custom-btn mb-2">Create Absence</v-btn>
      <v-card class="create-absance">
        <v-card-title>
          <span class="headline">Create Absence</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12 sm6 d-flex>
                <v-select :items="absenceReasonOptions" label="Reason" v-model="editedItem.reason"></v-select>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="editedItem.start_date" label="Start Data"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="editedItem.end_date" label="End Data"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="editedItem.notes" label="Notes"></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="close">Cancel</v-btn>
          <v-btn color="blue darken-1" flat @click="save">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <div class="absence-table">
      <v-toolbar flat color="white" class="table-header">
        <v-toolbar-title>My Absences</v-toolbar-title>
        <FiltersBar :setFilter="setFilter" />
      </v-toolbar>
      <v-data-table :headers="headers" :items="absences" class="elevation-2" hide-actions>
        <template slot="items" slot-scope="props">
          <td>{{ props.item.status }}</td>
          <td>{{ props.item.reason }}</td>
          <td class="text-xs-left">{{ props.item.start_date }}</td>
          <td class="text-xs-left">{{ props.item.end_date }}</td>
          <td class="text-xs-left">{{ props.item.notes }}</td>
          <td class="text-xs-left">
            <v-icon
              v-if="props.item.status === 'new'"
              small
              class="icon mr-2"
              @click="changeStatus(props.item, 'verifying')"
            >check_circle</v-icon>
            <v-icon
              v-if="props.item.status === 'new'"
              small
              class="icon mr-2"
              @click="editItem(props.item)"
            >edit</v-icon>
            <v-icon
              v-if="props.item.status === 'new'"
              small
              class="icon"
              @click="deleteItem(props.item)"
            >delete</v-icon>
            <v-icon
              v-if="props.item.status === 'verifying'"
              class="icon"
              small
              @click="changeStatus(props.item, 'new')"
            >block</v-icon>
          </td>
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
import * as absenceService from "../services/absence.service";
import { mapState, mapActions } from "vuex";
import * as config from "@/config.js";
import FiltersBar from "./FiltersBar";

export default {
  components: {
    FiltersBar
  },
  data: () => ({
    absenceReasonOptions: config.absenceReasonOptions,
    dialog: false,
    userProfile: {},
    headers: [
      { text: "Status", value: "status" },
      {
        text: "Reason",
        align: "left",
        sortable: true,
        value: "reason"
      },
      { text: "Start Data", value: "start_date" },
      { text: "End Data", value: "end_date" },
      { text: "Notes", value: "notes" },
      { text: "Actions", value: "name", sortable: false }
    ],
    editedIndex: -1,
    editedItem: {
      reason: "",
      start_date: 0,
      end_date: 0,
      notes: ""
    },
    defaultItem: {
      reason: "",
      start_date: 0,
      end_date: 0,
      notes: ""
    }
  }),
  computed: mapState({
    absences: state => state.absence.allAbsences,
    paginationInfo: state => state.absence.paginationInfo
  }),

  watch: {
    dialog(val) {
      val || this.close();
    },
    "paginationInfo.page"() {
      this.getAbsences();
    }
  },

  created() {
    this.getAbsences();
  },

  methods: {
    ...mapActions({
      getAbsences: "absence/getAbsences",
      setPaginationInfo: "absence/setPaginationInfo",
      setFilter: "absence/setFilter"
    }),

    onSetPagination(paginationInfo) {
      this.setPaginationInfo(paginationInfo);
    },

    editItem(item) {
      this.editedIndex = this.absences.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      absenceService.deleteAbsence(item.id).then(
        () => {
          this.getAbsences();
        },
        () => {}
      );
    },

    changeStatus(item, status) {
      absenceService.changeStatus(item.id, { status }).then(
        () => {
          this.getAbsences();
        },
        () => {}
      );
    },

    close() {
      this.dialog = false;
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      }, 300);
    },

    //make action
    save() {
      const data = {
        reason: this.editedItem.reason,
        start_date: this.editedItem.start_date,
        end_date: this.editedItem.end_date,
        notes: this.editedItem.notes,
        status: "new",
        user: { id: this.$store.state.user.logedUserId }
      };
      if (this.editedIndex == -1) {
        absenceService.createNewAbsence(data).then(
          () => {
            this.getAbsences("");
            this.close();
          },
          () => {}
        );
      } else {
        absenceService.editAbsence(data, this.editedItem.id).then(
          () => {
            this.getAbsences("");
            this.close();
          },
          () => {}
        );
      }
    }
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
.v-select__slot > label,
.theme--light.v-label,
.v-icon.material-icons.theme--light {
  background: #003851 !important;
  color: #66a4d4 !important;
}
.create-absance {
  background:  rgba(102, 164, 212, 1)!important;
 color: #66a4d4 !important;
}

</style>

