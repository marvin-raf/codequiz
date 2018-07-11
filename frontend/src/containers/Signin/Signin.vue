<template>
    <v-card class="col-lg-8 offset-lg-2" id="sign-in">
        <h1>Sign In</h1>

        <v-text-field type="text" label="Email" v-model="email" color="secondary" class="col-md-10 offset-md-1" :error-messages="errors.email" :maxlength="320"></v-text-field>

        <v-text-field type="password" label="Password" v-model="password" color="secondary" class="col-md-10 offset-md-1" :error-messages="errors.password" :maxlength="50"></v-text-field>

        <v-btn color="secondary" id="sign-in-btn" depressed @click="signIn()" :loading="loading">Sign Up</v-btn>
    </v-card>
</template>

<script>
import helpers from "./helpers";
import cookies from "js-cookie";

export default {
  data() {
    return {
      email: "",
      password: "",
      errors: {
        email: [],
        password: []
      },
      loading: false
    };
  },
  methods: {
    async signIn() {
      // Reset errors
      this.errors.email = [];
      this.errors.password = [];

      // Check for errors
      if (!this.email) {
        this.errors.email.push("Field Required");
      }

      if (!this.password) {
        this.errors.password.push("Field Required");
      }

      if (this.errors.email.length || this.errors.password.length) return;

      this.loading = true;

      try {
        const json = await helpers.signIn(this.email, this.password);
        console.log("Did I make it past here");

        if (json.teacher_id) {
          cookies.set("teacher", json.token);
        } else {
          cookies.set("student", json.token);
        }

        this.loading = false;
        this.$router.push("/dashboard");
      } catch (e) {
        console.log(e);
        this.loading = false;
        console.log("There was an error");
      }
    }
  }
};
</script>

<style lang="scss">
@import "../../styles/_mixins.scss";
@import "../../styles/_variables.scss";
#sign-in {
  background-color: #fff;
  h1 {
    text-align: center;
    color: $text-color;
  }
  @include card();
}

#sign-in-btn {
  display: block;
  margin: 0 auto;
}
</style>



