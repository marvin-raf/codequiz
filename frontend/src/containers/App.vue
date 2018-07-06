<template>
  <div id="app">
    <Sidebar/>

    
  </div>
</template>

<script>
import Sidebar from "./Sidebar/Sidebar";

export default {
  name: "app",
  components: {
    Sidebar
  },
  data() {
    return {};
  }
};
</script>

<style lang="scss">
@import "../styles/variables.scss";
@import "../styles/imports.scss";
html,
body {
  background-color: $background;
  font-family: "Roboto";
  height: 100%;
}

#app {
  height: 100%;
}

h1,
h2,
h3,
h4,
h5,
h6,
p,
span {
  opacity: 0.87;
}
</style>
