<template>
  <div class="login-main-container">
    <v-layout align-center justify-center row fill-height>
      <div class="login-container">
        <img src="@/assets/logo.svg" alt="Vue Logo" height="100" width="250" />
        <v-card class="content-container">
          <v-form>
            <div class="title-form">Log In</div>
            <v-container>
              <v-layout>
                <v-flex xs12 md6>
                  <v-text-field v-model="email" :counter="10" label="Email" required></v-text-field>
                </v-flex>
                <v-flex xs12 md6>
                  <v-text-field
                    type="password"
                    v-model="password"
                    :counter="10"
                    label="Password"
                    required
                  ></v-text-field>
                </v-flex>
              </v-layout>
              <div v-if="this.error" class="error-login">{{this.error}}!</div>
              <div class="button-container">
                <v-btn class="button" @click="makeLogin">Log in</v-btn>
              </div>
            </v-container>
          </v-form>
        </v-card>
      </div>
    </v-layout>
  </div>
</template>

<script>
import { mapActions } from "vuex";
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
      getUserProfile: "user/getUser"
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
.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.login-main-container {
  margin-top: 10px;
  height: 100%;
}

.theme--light.v-sheet.content-container {
  background: #003851;
  border-radius: 3px;
  padding: 20px;
}

.error-login {
  color: red;
}

.title-form {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  font-size: 25px;
  color: #66a4d4;
}

.v-form > .container {
  padding: 22px;
}
.theme--light.v-label,
.theme--light.v-counter {
  color: #66a4d4;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
.button {
  background-color: #66a4d4 !important;
  border-color: #66a4d4 !important;
  color: white !important;
}
</style>
