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
    data: () => ({
      userId: null,
    }),
    created () {
      this.getUserId();
    },
    mounted () {
      this.userId = this.$store.state.user.logedUserId;
    },
     methods: {
      getUserId() {
        this.$store.dispatch('user/setUserId');
        if (this.$store.state.user.logedUserId) {
            this.$router.push('/UserPage');
        }
        else {
          this.$router.push('/Login');
        }
      },
     }
  }
</script>

<style>

</style>
