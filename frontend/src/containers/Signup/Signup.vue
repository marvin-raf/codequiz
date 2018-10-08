<template>
  <v-card class="col-lg-8 offset-lg-2" id="sign-up">
    <h1>Sign Up</h1>

    <v-text-field type="text" label="Name" v-model="name" color="secondary" class="col-md-10 offset-md-1" :error-messages="errors.name" :maxlength="50" append-icon="keyboard-arrow-down"></v-text-field>

    <v-text-field type="text" label="Location" v-model="email" color="secondary" class="col-md-10 offset-md-1" :error-messages="errors.email" :maxlength="320"></v-text-field>
    <!-- <div class="col-md-10 offset-md-1">
      <div style="float: left; width: 70%;">
        <v-text-field type="text" label="Name" v-model="confirmPassword" color="secondary" :error-messages="errors.confirmPassword" :maxlength="50" style="margin-left: 2px;"></v-text-field>
      </div>

      <div style="float: left; width: 26%;margin-left: 5px;">
        <v-text-field type="text" label="Time" color="secondary"> </v-text-field>
      </div>
    </div> -->
    <v-btn color="secondary" id="sign-up-btn" class="col-md-10 offset-md-1" depressed @click="signUp()" :loading="loading">Create</v-btn>

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
        this.$router.push("/dashboard");
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
  padding-bottom: 20px;
}

#sign-up-btn {
  display: block;
  margin: 0 auto;
  width: 100%;
}
</style>

