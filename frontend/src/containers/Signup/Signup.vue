<template>
<v-card class="col-lg-8 offset-lg-2" id="signup">
    <h1>Signup</h1>

    <v-text-field type="text" label="Name" v-model="name" color="secondary" class="col-md-10 offset-md-1" :error-messages="nameErrors"></v-text-field> 

    <v-text-field type="text" label="Email" v-model="email" color="secondary" class="col-md-10 offset-md-1" :error-messages="emailErrors"></v-text-field>

    <v-text-field type="password" label="Password" v-model="password" color="secondary" class="col-md-10 offset-md-1" :error-messages="passwordErrors"></v-text-field>

    <v-text-field type="password" label="Confirm Password" v-model="confirmPassword" class="col-md-10 offset-md-1" color="secondary" :error-messages="confirmPasswordErrors"></v-text-field>

    <v-btn color="secondary" id="sign-up-btn" depressed @click="signUp()">Sign Up</v-btn>


    </v-card>
</template>

<script>
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
      }
    };
  },
  methods: {
    signUp() {
      this.resetErrors();
    },
    resetErrors() {
      for (key of Object.keys(this.errors)) {
        this.errors[key] = [];
      }
    }
  }
};
</script>


<style lang="scss">
@import "../../styles/_mixins.scss";
@import "../../styles/_variables.scss";
#signup {
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

