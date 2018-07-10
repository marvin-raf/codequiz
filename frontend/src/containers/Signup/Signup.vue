<template>
<v-card class="col-lg-8 offset-lg-2" id="sign-up">
    <h1>Sign Up</h1>

    <v-text-field type="text" label="Name" v-model="name" color="secondary" class="col-md-10 offset-md-1" :error-messages="errors.name" :maxlength="50"></v-text-field> 

    <v-text-field type="text" label="Email" v-model="email" color="secondary" class="col-md-10 offset-md-1" :error-messages="errors.email" :maxlength="320"></v-text-field>

    <v-text-field type="password" label="Password" v-model="password" color="secondary" class="col-md-10 offset-md-1" :error-messages="errors.password" :maxlength="50"></v-text-field>

    <v-text-field type="password" label="Confirm Password" v-model="confirmPassword" class="col-md-10 offset-md-1" color="secondary" :error-messages="errors.confirmPassword" :maxlength="50"></v-text-field>

    <v-btn color="secondary" id="sign-up-btn" depressed @click="signUp()" :loading="loading">Sign Up</v-btn>


    </v-card>
</template>

<script>
import helpers from "./helpers.js";
import cookies from "js-cookie";

export default {
  data() {
    return {
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
      errors: {
        name: [],
        email: [],
        password: [],
        confirmPassword: []
      },
      loading: false
    };
  },
  methods: {
    async signUp() {
      this.resetErrors();

      if (helpers.formHasErrors(this)) return;

      this.loading = true;

      try {
        await helpers.signUp({
          name: this.name,
          email: this.email,
          password: this.password,
          errors: this.errors
        });

        const token = await helpers.signIn({
          email: this.email,
          password: this.password
        });

        cookies.set("teacher", token);

        this.loading = false;
        this.$router.push("/profile/dashboard");
      } catch (e) {
        this.loading = false;
      }
    },
    resetErrors() {
      for (const key of Object.keys(this.errors)) {
        this.errors[key] = [];
      }
    }
  }
};
</script>


<style lang="scss">
@import "../../styles/_mixins.scss";
@import "../../styles/_variables.scss";
#sign-up {
  background-color: #fff;
  h1 {
    text-align: center;
    color: $text-color;
  }
  @include card();
}

#sign-up-btn {
  display: block;
  margin: 0 auto;
}
</style>

