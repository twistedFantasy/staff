<template>
  <div class='profile'>
    <div class='row'>
      <div class='field'> Email :</div>
      <div class='value'> {{userProfile.email}}</div>
    </div>
    
  </div>
</template>

<script>
  import { mapState, mapGetters } from 'vuex';
  export default {
     data: () => ({
    }),
    computed: {
      ...mapGetters('user', { userProfile: 'getUserProfile'})
    }
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
