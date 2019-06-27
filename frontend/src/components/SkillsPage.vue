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
  }),
  computed: {
    ...mapGetters("user", { userProfile: "getUserProfile" })
  },
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
