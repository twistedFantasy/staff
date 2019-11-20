<template>
  <div class="create-absence">
    <v-dialog class="dialog" v-model="dialog" max-width="500px">
      <v-btn slot="activator" color="primary" dark class="custom-btn mb-2">Create Absence</v-btn>
      <v-card class="create-absence-dialog">
        <v-card-title>
          <span class="headline">Create Absence</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12 sm6 d-flex>
                <v-select :items="absenceReasonOptions" label="Reason" v-model="editedItem.reason"></v-select>
              </v-flex>
              <v-flex xs12 sm6 d-flex>
                <v-menu
                  ref="menu1"
                  :close-on-content-click="false"
                  v-model="menu1"
                  :nudge-right="40"
                  :return-value.sync="editedItem.start_date"
                  lazy
                  transition="scale-transition"
                  offset-y
                  full-width
                  min-width="390px"
                >
                  <v-text-field
                    slot="activator"
                    v-model="editedItem.start_date"
                    label="Start date"
                    prepend-icon="event"
                    readonly
                  ></v-text-field>
                  <v-date-picker
                    v-model="editedItem.start_date"
                    @input="$refs.menu1.save(editedItem.start_date)"
                  ></v-date-picker>
                </v-menu>
              </v-flex>
              <v-flex xs12 sm6 d-flex>
                <v-menu
                  ref="menu2"
                  :close-on-content-click="false"
                  v-model="menu2"
                  :nudge-right="40"
                  :return-value.sync="editedItem.end_date"
                  lazy
                  transition="scale-transition"
                  offset-y
                  full-width
                  min-width="390px"
                >
                  <v-text-field
                    slot="activator"
                    v-model="editedItem.end_date"
                    label="End date"
                    prepend-icon="event"
                    readonly
                  ></v-text-field>
                  <v-date-picker
                    v-model="editedItem.end_date"
                    @input="$refs.menu2.save(editedItem.end_date)"
                  ></v-date-picker>
                </v-menu>
              </v-flex>
              <v-flex xs12 sm6 d-flex>
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
  </div>
</template>

<script>
import * as absenceService from "@/services/absence.service";
import { mapState, mapActions } from "vuex";
import * as config from "@/config.js";

export default {
  props: {
    getAbsences: { type: Function }
  },
  data: () => ({
    absenceReasonOptions: config.absenceReasonOptions,
    dialog: false,
    editedIndex: -1,
    editedItem: {
      reason: "",
      start_date: null,
      end_date: null,
      notes: ""
    },
    defaultItem: {
      reason: "",
      start_date: null,
      end_date: null,
      notes: ""
    },
    menu1: false,
    menu2: false
  }),

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  methods: {
    editItem(item) {
      this.editedIndex = this.absences.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
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
</script>

<style>
.v-card__text {
  background-color: #99bfdc !important;
  color: #001c29 !important;
}
.create-absence .v-btn__content {
  color: #001c29;
}
.create-absence-dialog {
  background-color: #99bfdc !important;
  color: #001c29 !important;
}
.create-absence .theme--light.v-select .v-select__selections {
  color: #001c29 !important;
}
.create-absence-dialog .theme--light.v-select .v-select__selections,
.theme--light.v-label {
  color: #001c29 !important;
}
.create-absence-dialog .blue--text.text--darken-1 {
  color: #001c29 !important;
}
.v-list .theme--light {
  background: #c2e4ff !important;
}
</style>


    