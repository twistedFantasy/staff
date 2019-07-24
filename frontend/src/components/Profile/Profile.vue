<template>
  <div class="profile">
    <EditProfileForm />
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
  </div>
</template>
<script>

import { mapGetters } from "vuex";
import SkillsPage from "./SkillsPage";
import EditProfileForm from "./EditProfileForm";

export default {
  components: {
    SkillsPage,
    EditProfileForm,
  },
  data: () => ({
   
  }),
  computed: {
    ...mapGetters("user", { userProfile: "getUserProfile" })
  },
};
</script>

<style>
.profile {
  padding: 20px 40px;
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