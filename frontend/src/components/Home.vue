<template>
  <v-container>
    <v-layout
      text-xs-center
      wrap
    >
      <v-flex xs12>
        <v-img
          :src="require('../assets/logo.svg')"
          class="my-3"
          contain
          height="200"
        ></v-img>
      </v-flex>

      <v-flex mb-4>
        <h1 class="display-2 font-weight-bold mb-3">
          Welcome to Codex
          {{user}}
        </h1>
        <p class="subheading font-weight-regular">
          Here you can celebrate your holidays and sick leave.
        </p>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  export default {
    computed: {
    user() {
      return this.$store.state.userProfile;
     // console.log(user.name, 'user');
    }
    }
  }
</script>

<style>

</style>
