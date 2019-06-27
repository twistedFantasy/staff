<template>
  <div class="profile">
    <v-dialog v-model="dialog" max-width="800px">
      <v-btn slot="activator" color="primary" dark class="mb-2">Edit</v-btn>
      <v-card>
        <v-card-title>
          <span class="headline">Edit</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12 sm6 d-flex>
                <v-text-field label="full name" v-model="editedItem.full_name"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="editedItem.skype" label="skype"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="editedItem.phone_number" label="phone_number"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="editedItem.phone_number2" label="phone_number2"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="editedItem.date_of_birth" label="date_of_birth"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="editedItem.education" label="education"></v-text-field>
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

    <div class="row">
      <div class="field">Phone number :</div>
      <div class="value">{{userProfile.phone_number}}</div>
    </div>
    <div class="row">
      <div class="field">Skype :</div>
      <div class="value">{{userProfile.skype}}</div>
    </div>
    <div class="row">
      <div class="field">Date of birth :</div>
      <div class="value">{{userProfile.date_of_birth}}</div>
    </div>
    <div class="row">
      <div class="field">Education :</div>
      <div class="value">{{userProfile.education}}</div>
    </div>
    <div class="row">
      <div class="field">Has card :</div>
      <div class="value">{{userProfile.has_card ? 'yes' : 'no'}}</div>
    </div>
    <div class="row">
      <div class="field">Has key :</div>
      <div class="value">{{userProfile.has_key ? 'yes' : 'no'}}</div>
    </div>
    <SkillsPage/>
    <v-btn fab dark color="cyan">
      <v-icon dark>edit</v-icon>
    </v-btn>
  </div>
</template>

<script>
import { mapState, mapGetters } from "vuex";
import * as authService from "../services/auth.service";
import SkillsPage from "./SkillsPage";
export default {
  components: {
    SkillsPage
  },
  data: () => ({
    dialog: false,
    editedItem: {
      full_name: "",
      skype: "",
      phone_number: "",
      phone_number2: "",
      date_of_birth: "",
      education: ""
    },
  }),
  computed: {
    ...mapGetters("user", { userProfile: "getUserProfile" })
  },
  created() {
    this.editedItem = {
      full_name: this.userProfile.full_name,
      skype: this.userProfile.skype,
      phone_number: this.userProfile.phone_number,
      phone_number2: this.userProfile.phone_number2,
      date_of_birth: this.userProfile.date_of_birth,
      education: this.userProfile.education
    };
  },
  methods: {
    close() {
      this.dialog = false;
      setTimeout(() => {}, 300);
    },
    // move creational modal to difference component
    //make action
    save() {
      const data = {
        phone_number: this.editedItem.phone_number,
        phone_number2: this.editedItem.phone_number2,
        full_name: this.editedItem.full_name,
        skype: this.editedItem.skype,
        date_of_birth: this.editedItem.date_of_birth,
        education: this.editedItem.education
      };
      //sent only editinal field
      // add edit skills const newProfile = { skills: [...userProfile.skills] };
      const userId = this.$store.state.user.logedUserId;
      authService.updateUserProfile(userId, data).then(
        () => {
          //this.getUserProfile();
          this.close();
        },
        error => {
          console.log(error, "error");
        }
      );
    }
  }
};
</script>

<style>
.profile {
  padding: 20px;
}
.row {
  margin: 10px 0;
  display: flex;
  align-items: center;
}
.field {
  font-size: 19px;
}
.value {
  font-size: 16px;
  margin-left: 10px;
}
</style>
