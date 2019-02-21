<template>
  <div class='profile'>
    <div class='row'>
      <div class='field'> Email :</div>
      <div class='value'> {{userProfile.email}}</div>
    </div>
    <div class='row'>
      <div class='field'> Phone number : </div>
      <div class='value'>{{userProfile.phone_number}}</div>
    </div>
    <div class='row'>
      <div class='field'>Skype : </div>
      <div class='value'>{{userProfile.skype}}</div>
    </div>
    <div class='row'>
      <div class='field'>Date of birth : </div>
      <div class='value'>{{userProfile.date_of_birth}}</div>
    </div>
    <div class='row'>
      <div class='field'>Education : </div>
      <div class='value'>{{userProfile.education}}</div>
    </div>
  </div>
</template>

<script>
  import * as authService from '../services/auth.service'
  export default {
     data: () => ({
      userProfile: {},
    }),
     mounted () {
      this.userProfile = this.$store.state.user.userProfile;
    },
 
  }
</script>

<style>
.profile {
  padding: 40px;
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
