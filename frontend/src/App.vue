<template>
  <v-app id="app">
    <v-toolbar app>
      <v-toolbar-side-icon></v-toolbar-side-icon>
      <v-toolbar-title>Title</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-sm-and-down toolbar-right">
        <router-link to="/Login">
          <i aria-hidden="true" @click="makeLogout" class="v-icon mdi mdi-account"></i>
        </router-link>
      </v-toolbar-items>
    </v-toolbar>
    <v-content>
      <router-view/>
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      //
    };
  },
  created() {
    this.getUserId();
  },
  methods: {
    getUserId() {
      this.$store.dispatch("user/setUserId");
      if (this.$store.state.user.logedUserId) {
        this.$router.push("/Home");
      } else {
        this.$router.push("/Login");
      }
    },
    makeLogout() {
      localStorage.removeItem("user");
    }
  }
};
</script>

<style>
.hidden-sm-and-down.toolbar-right {
  padding: 15px;
}
.mail {
  margin-right: 25px;
}
</style>
