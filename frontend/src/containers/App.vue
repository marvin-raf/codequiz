<template>
  <div id="app">
    <Notification />
    <Sidebar id="sidebar" />

    <div id="router-view">
      <v-app>
        <router-view></router-view>
      </v-app>
    </div>

  </div>
</template>

<script>
import Sidebar from "./Sidebar/Sidebar";
import Notification from "../components/Notification/Notification.vue"

export default {
  name: "app",
  components: {
    Sidebar,
    Notification
  },
  data() {
    return {
    };
  }
};
</script>

<style lang="scss">
@import "../styles/_variables.scss";
@import "../styles/_imports.scss";
html,
body {
  font-family: "Roboto";
  height: 100%;
  background-color: $background;
}

#app {
  height: 100%;
  background-color: $background;
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

#sidebar {
  float: left;
}

#router-view {
  height: 100%;
  position: relative;
  width: calc(100% - 200px);
  margin-left: 200px;
  float: left;
  background-color: $background !important;
}
</style>
