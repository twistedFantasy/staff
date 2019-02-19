<template>
  <div class="container">
  <v-layout align-center justify-center row fill-height>
    <v-card>
    <v-form >
      <div class="title-form"> Log In</div>
    <v-container>
      <v-layout>
        <v-flex
          xs12
          md6
        >
          <v-text-field
            v-model="email"
            :counter="10"
            label="Email"
            required
          ></v-text-field>
        </v-flex>
        <v-flex
          xs12
          md6
        >
          <v-text-field
            v-model="password"
            :counter="10"
            label="Password"
            required
          ></v-text-field>
        </v-flex>
      </v-layout>
      <div v-if="this.error" class="error-login">{{this.error}}!</div>
      <div class="button-container">
        <v-btn color="success" @click="makeLogin">
          Log in
        </v-btn>
      </div>
      
    </v-container>
  </v-form>
    </v-card>
  </v-layout>
  </div>
</template>

<script>
 import * as authService from '../services/auth.service'
 import { setUserId } from '../store/modules/user';
 import { mapState } from 'vuex'

export default {
  data () {
    return {
      email: '',
      password: '',
      error: '',
    }
  },
  methods: {
    getUserProfile(userId) {
      const responce = authService.getUserById(userId).then(
        data => {
            this.$store.dispatch('user/setUser', data)
        },
        error => {
          console.log(error, 'error')
        }
      );
    },
    makeLogin () {
       const responce = authService.makeLogin(this.email, this.password).then(
        data => {
            this.error = null;
             this.$store.dispatch('user/setUserId', data.user)
             this.$router.push('/UserPage');
             this.getUserProfile(data.user);
        },
        error => {
          this.error = error;
        }
      );
    },
  } 
}
</script>

<style>
.container {
  margin-top: 10px;
  
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
.v-form>.container {
  padding: 22px;
}
.button-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}


</style>
