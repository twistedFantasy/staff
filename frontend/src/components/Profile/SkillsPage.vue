<template>
  <div>
    <div class="skills">
      <div v-for="skill in userProfile.skills" v-bind:key="skill.name">
        <div class="text-xs-center">
          <v-chip outline color="primary">{{ skill.name }}</v-chip>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  data: () => ({}),
  computed: mapState({
    userProfile: state => state.user.userProfile
  })
};
</script>

<style>
.edit-icon {
  cursor: pointer;
}
.skills {
  display: flex;
}
.skills .v-chip__content {
  color: #66a4d4 !important;
}
</style>
