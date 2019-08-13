<template>
  <div class="login">
    <Login />
  </div>
</template>

<script>
// @ is an alias to /src
import Login from "@/components/Login.vue";

export default {
  name: "login",
  components: {
    Login
  }
};
</script>

<style>
.login {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>