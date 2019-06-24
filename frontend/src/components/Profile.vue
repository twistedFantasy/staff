<template>
  <div class="profile">
    <div class="row">
      <div class="field">Email :</div>
      <div class="value">{{userProfile.email}}</div>
    </div>
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
import SkillsPage from "./SkillsPage";
export default {
  components: {
    SkillsPage
  },
  data: () => ({}),
  computed: {
    ...mapGetters("user", { userProfile: "getUserProfile" })
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
