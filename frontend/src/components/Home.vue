<template>
  <v-container>
    <div v-if="userId"><UserPage/></div>
    <div v-if="!userId"><Login/></div>
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
      },
     }
  }
</script>

<style>

</style>
