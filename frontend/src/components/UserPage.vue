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
            <span class="headline">{{ formTitle }}</span>
          </v-card-title>

          <v-card-text>
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex xs12 sm6 md4>
                  <v-text-field v-model="editedItem.name" label="Reason"></v-text-field>
                </v-flex>
                <v-flex xs12 sm6 md4>
                  <v-text-field v-model="editedItem.calories" label="Start Data"></v-text-field>
                </v-flex>
                <v-flex xs12 sm6 md4>
                  <v-text-field v-model="editedItem.fat" label="End Data"></v-text-field>
                </v-flex>
                <v-flex xs12 sm6 md4>
                  <v-text-field v-model="editedItem.carbs" label="Notes"></v-text-field>
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
import { mapState } from 'vuex'
 import * as absenceService from '../services/absence.service'

  export default {
    data: () => ({
      dialog: false,
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
        name: '',
        calories: 0,
        fat: 0,
        carbs: 0,
        protein: 0
      },
      defaultItem: {
        name: '',
        calories: 0,
        fat: 0,
        carbs: 0,
        protein: 0
      }
    }),

    computed: mapState({
    absence: state => state.absence.allAbsences,
  }),
    watch: {
      dialog (val) {
        val || this.close()
      }
    },
    created () {
      this.getAbsence()
    },
    methods: {
        getAbsence() {
        const responce = absenceService.getAllAbsencesByUserId().then(
          data => {
             this.$store.dispatch('absence/setAllAbsence', data.results)
             this.absences= data.results;
             console.log(JSON.parse(JSON.stringify(this.absence)), 'all');
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
        if (this.editedIndex > -1) {
          Object.assign(this.desserts[this.editedIndex], this.editedItem)
        } else {
          this.desserts.push(this.editedItem)
        }
        this.close()
      }
    },
  }
</script>

<style>
 td {
 }

</style>
