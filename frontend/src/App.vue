<template>
  <v-app class="app" id="app">
    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "App",
  data() {
    return {
      //
    };
  },
  computed: mapState({
    userProfile: state => state.user.userProfile
  }),
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
#app {
  background: #001c29;
  color: #66A4D4;
}
.hidden-sm-and-down.toolbar-right {
  padding: 15px;
}
.mail {
  margin-right: 25px;
}
</style>
