<template>
  <v-container>
  </v-container>
</template>

<script>
import UserPage from "@/components/UserPage.vue";
import Login from "@/components/Login.vue";
  export default {
    components: {
      UserPage,
      Login,
    },
    created () {
      if (this.$store.state.user.logedUserId) {
          this.$router.push('/UserPage');
      }
        else {
          this.$router.push('/Login');
      }
    },
  }
</script>

<style>

</style>
