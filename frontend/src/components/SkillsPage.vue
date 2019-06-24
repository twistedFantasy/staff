<template>
  <div>
    <div class="skills">
      <div v-for="skill in userProfile.skills" v-bind:key="skill.name">
        <div class="text-xs-center">
          <v-chip outline color="primary">
            {{ skill.name }}
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
