<template>
  <div class="absence-table">
    <v-toolbar flat color="white">
      <v-toolbar-title>My Absences</v-toolbar-title>
      <v-divider
        class="mx-2"
        inset
        vertical
      ></v-divider>
      <v-spacer></v-spacer>
      <v-dialog v-model="dialog" max-width="500px">
        <v-btn slot="activator" color="primary" dark class="mb-2">Create Absence</v-btn>
        <v-card>
          <v-card-title>
            <span class="headline">Create Absence</span>
          </v-card-title>
          <v-card-text>
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex xs12 sm6 d-flex>
                  <v-select
                    :items="absenceReasonOptions"
                    label="Reason"
                    v-model="editedItem.reason"
                  ></v-select>
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
    </v-toolbar>
    <v-data-table
      :headers="headers"
      :items="absences"
      class="elevation-1"
    >
      <template slot="items" slot-scope="props">
        <td>{{ props.item.reason }}</td>
        <td class="text-xs-left">{{ props.item.start_date }}</td>
        <td class="text-xs-left">{{ props.item.end_date }}</td>
        <td class="text-xs-left">{{ props.item.notes }}</td>
        <td class="justify-center layout px-0">
          <v-icon
            small
            class="mr-2"
            @click="editItem(props.item)"
          >
            edit
          </v-icon>
          <v-icon
            small
            @click="deleteItem(props.item)"
          >
            delete
          </v-icon>
        </td>
      </template>
      <template slot="no-data">
        <v-btn color="primary" @click="getAbsence">Reset</v-btn>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import * as absenceService from '../services/absence.service';
import * as config from '@/config.js';

  export default {
    data: () => ({
      dialog: false,
      absenceReasonOptions: config.absenceReasonOptions,
      headers: [
        {
          text: 'Reason',
          align: 'left',
          sortable: false,
          value: 'name'
        },
        { text: 'Start Data', value: 'calories' },
        { text: 'End Data', value: 'fat' },
        { text: 'Notes', value: 'carbs' },
        { text: 'Actions', value: 'name', sortable: false }
      ],
      absences: [],
      editedIndex: -1,
      editedItem: {
        reason: '',
        start_date: 0,
        end_date: 0,
        notes: ''
      },
      defaultItem: {
        reason: '',
        start_date: 0,
        end_date: 0,
        notes: ''
      }
    }),

    watch: {
      dialog (val) {
        val || this.close()
      }
    },
    created () {    
      this.getAbsence();
    },
    methods: {
      getAbsence() {
        absenceService.getAllAbsencesByUserId().then(
          data => {
             this.$store.dispatch('absence/setAllAbsence', data.results)
             this.absences= data.results;
          },
          error => {
            console.log(error, 'error')
          }
        );
      },
       editItem (item) {
         console.log(item, 'editItem')
       /* this.editedIndex = this.desserts.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
        */
      },
      deleteItem (item) {
        console.log(item, 'deleteItem')
        /*
        const index = this.desserts.indexOf(item)
        confirm('Are you sure you want to delete this item?') && this.desserts.splice(index, 1)
        */
      },
      close () {
        this.dialog = false
        setTimeout(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        }, 300)
      },
      save () {
        const data = {
          reason: this.editedItem.reason,
          start_date: this.editedItem.start_date,
          end_date: this.editedItem.end_date,
          notes: this.editedItem.notes,
        }
        absenceService.createNewAbsence(data).then(
          data => {
            this.getAbsence();
            this.close();
          },
          error => {
            console.log(error, 'error')
          }
        );
      }
    },
  }
</script>

<style>
  .absence-table {
    margin: 40px;
  }

</style>
