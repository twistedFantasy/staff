<template>
  <div class="profile">
    <v-dialog v-model="dialog" max-width="500px">
      <v-btn slot="activator" flat icon color="primary lighten-2">
        <v-icon>add</v-icon>
      </v-btn>
      <v-card>
        <v-card-title>
          <span class="headline">Create New Skill</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="newSkill" label="Name of Skill"></v-text-field>
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
    <div class="skills">
      <div v-for="skill in userProfile.skills" v-bind:key="skill.name">
        <div class="text-xs-center">
          <v-chip outline color="primary" close @input="deleteSkill(skill.name)">
            {{ skill.name }}
            <v-icon @click="edit(skill.name)" class="edit-icon" size="20" right>edit</v-icon>
          </v-chip>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from "vuex";
import * as authService from "../services/auth.service";
export default {
  data: () => ({
    newSkill: "",
    editSkill: "",
    dialog: false
  }),
  computed: {
    ...mapGetters("user", { userProfile: "getUserProfile" })
  },
  methods: {
    deleteSkill(name) {
      console.log("delete");
    },

    edit(name) {
      this.newSkill = name;
      this.editSkill = name;
      this.dialog = true;
    },

    close() {
      this.dialog = false;
      setTimeout(() => {
        this.newSkill = "";
      }, 300);
    },

    getUserProfile() {
      authService.getUserById(this.$store.state.user.logedUserId).then(
        data => {
          this.$store.dispatch("user/setUser", data);
        },
        error => {
          console.log(error, "error");
        }
      );
    },

    save() {
      const userProfile = JSON.parse(
        JSON.stringify(this.$store.state.user.userProfile)
      );
      const currentSkill = userProfile.skills.find(
        skill => skill.name === this.editSkill
      );
      const index = userProfile.skills.indexOf(currentSkill);
      if (index >= 0) {
        userProfile.skills.splice(index, 1, { name: this.newSkill });
      } else {
        userProfile.skills.push({ name: this.newSkill });
      }
      const userId = this.$store.state.user.logedUserId;
      const newProfile = { skills: [...userProfile.skills] };
      if (this.newSkill) {
        authService.createNewSkill(userId, newProfile).then(
          () => {
            this.getUserProfile();
            this.close();
            this.editSkill = "";
          },
          error => {
            console.log(error, "error");
          }
        );
      }
    }
  }
};
</script>

<style>
.edit-icon {
  cursor: pointer;
}
.skills {
  display: flex;
}
</style>
