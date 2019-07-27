<template>
<div class="edit-profile-form">
  <v-dialog v-model="dialog" max-width="800px">
    <v-btn slot="activator" small class="mb-2" fab dark color="indigo">
      <v-icon dark>edit</v-icon>
    </v-btn>
    <v-card>
      <v-card-title>
        <span class="headline">Edit Profile</span>
      </v-card-title>

      <v-card-text>
        <v-container grid-list-md>
          <v-layout wrap>
            <v-flex xs12 sm6 d-flex>
              <v-text-field label="full name" v-model="editedItem.full_name"></v-text-field>
            </v-flex>
            <v-flex xs12 sm6 d-flex>
              <v-text-field v-model="editedItem.skype" label="skype"></v-text-field>
            </v-flex>
            <v-flex xs12 sm6 d-flex>
              <v-text-field v-model="editedItem.phone_number" label="phone_number"></v-text-field>
            </v-flex>
            <v-flex xs12 sm6 d-flex>
              <v-text-field v-model="editedItem.phone_number2" label="phone_number2"></v-text-field>
            </v-flex>
            <v-flex xs12 sm6 d-flex>
              <v-text-field v-model="editedItem.date_of_birth" label="date_of_birth"></v-text-field>
            </v-flex>
            <v-flex xs12 sm6 d-flex>
              <v-text-field v-model="editedItem.education" label="education"></v-text-field>
            </v-flex>
            <div class="edit-skill-container">
              <div v-for="skill in userProfile.skills" v-bind:key="skill.name">
                <div class="text-xs-center">
                  <v-chip
                    outline
                    color="primary"
                    close
                    @input="deleteSkill(skill.name)"
                  >{{ skill.name }}</v-chip>
                </div>
              </div>
              <div class="edit-skill-input" v-if="addSkillMode">
                <v-flex s12 sm6 d-flex>
                  <v-text-field
                    v-on:keyup.enter="createNewSkill()"
                    clearable
                    v-model="editedItem.newSkill"
                    label="new skill"
                  ></v-text-field>
                </v-flex>
                <v-btn @click="editSkillsMode" fab dark small color="indigo">
                  <v-icon dark>close</v-icon>
                </v-btn>
              </div>
              <v-btn v-else @click="editSkillsMode" fab dark small color="indigo">
                <v-icon dark>add</v-icon>
              </v-btn>
            </div>
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

import { mapState, mapActions } from "vuex";

export default {
  data: () => ({
    dialog: false,
    addSkillMode: false,
    editedItem: {
      full_name: "",
      skype: "",
      phone_number: "",
      phone_number2: "",
      date_of_birth: "",
      education: "",
      skills: [],
      newSkill: ""
    }
  }),
  computed: mapState({
    userProfile: state => state.user.userProfile,
    userId: state => state.user.logedUserId,
  }),
  created() {
    this.editedItem = {
      full_name: this.userProfile.full_name,
      skype: this.userProfile.skype,
      phone_number: this.userProfile.phone_number,
      phone_number2: this.userProfile.phone_number2,
      date_of_birth: this.userProfile.date_of_birth,
      education: this.userProfile.education,
      skills: this.userProfile.skills
    };
  },
  methods: {
    close() {
      this.dialog = false;
      setTimeout(() => {}, 300);
    },

    editSkillsMode() {
      this.addSkillMode = !this.addSkillMode;
      this.editedItem.newSkill = "";
    },
    createNewSkill() {
      this.editedItem.skills.push({ name: this.editedItem.newSkill });
      this.editedItem.newSkill = "";
      this.editSkillsMode();
    },
    deleteSkill(name) {
      const { editedItem } = this;
      const currentSkill = editedItem.skills.find(skill => skill.name === name);
      const index = editedItem.skills.indexOf(currentSkill);
      if (index >= 0) {
        editedItem.skills.splice(index, 1);
      }
    },
    ...mapActions({
      onChangeUserProfile: 'user/onChangeUserProfile'
    }),

    save() {
      this.onChangeUserProfile(this.editedItem);
      this.close(); 
    }
  }
};
</script>

<style>
.edit-skill-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
.edit-skill-input {
  display: flex;
  justify-content: center;
  align-items: center;
}
.edit-profile-form .v-dialog__container {
  display: flex!important;
  width: 100%;
  justify-content: flex-end;
}

</style>
