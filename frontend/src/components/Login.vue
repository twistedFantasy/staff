<template>
  <div class="container">
    <v-layout align-center justify-center row fill-height>
      <v-card class="content-container">
        <v-form>
          <div class="title-form">Log In</div>
          <v-container>
            <v-layout>
              <v-flex xs12 md6>
                <v-text-field v-model="email" :counter="10" label="Email" required></v-text-field>
              </v-flex>
              <v-flex xs12 md6>
                <v-text-field v-model="password" :counter="10" label="Password" required></v-text-field>
              </v-flex>
            </v-layout>
            <div v-if="this.error" class="error-login">{{this.error}}!</div>
            <div class="button-container">
              <v-btn color="success" @click="makeLogin">Log in</v-btn>
            </div>
          </v-container>
        </v-form>
      </v-card>
    </v-layout>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import * as authService from "../services/auth.service";

export default {
  data() {
    return {
      email: "",
      password: "",
      error: ""
    };
  },
  methods: {
    ...mapActions({
      getUserProfile: 'user/getUser'
    }),
    makeLogin() {
      authService
        .makeLogin(this.email, this.password)
        .then(data => {
          this.error = null;
          localStorage.setItem("user", data.token);
          this.$store.dispatch("user/setUserId", data.user);
          this.$router.push("/Home");
          this.getUserProfile();
        })
        .catch(error => (this.error = error));
    }
  }
};
</script>

<style>
.container {
  margin-top: 10px;
  
}
.theme--light.v-sheet.content-container {
  background: #003851;
  border-radius: 3px;
}
.error-login {
  color: red;
}
.title-form {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  font-size: 25px;
}
.v-form > .container {
  padding: 22px;
}
.button-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
