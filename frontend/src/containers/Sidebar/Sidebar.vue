<template>
    <v-navigation-drawer
    id="sidebar"
    dark
    permanent
  >
    <v-list>
      <v-list-tile
        v-for="item in authItems"
        :key="item.title"
        @click=""
      >
        <v-list-tile-action>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-tile-action>

        <v-list-tile-content>
          <v-list-tile-title>{{ item.title }}</v-list-tile-title>
        </v-list-tile-content>

      </v-list-tile>
        <v-divider></v-divider>

      <v-list-tile
        v-for="item in otherItems"
        :key="item.title"
        @click=""
      >
        <v-list-tile-action>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-tile-action>

        <v-list-tile-content>
          <v-list-tile-title>{{ item.title }}</v-list-tile-title>
        </v-list-tile-content>

      </v-list-tile>


    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  data() {
    return {
      authItems: [
        {
          title: "Signup",
          url: "/signup",
          icon: "lock"
        },
        {
          title: "Signin",
          url: "/signin",
          icon: "lock"
        }
      ],
      otherItems: [
        {
          title: "Quizzes",
          url: "/quizzes",
          icon: "pen"
        },
        {
          title: "About",
          url: "/about",
          icon: ""
        }
      ]
    };
  }
};
</script>


<style lang="scss" scoped>
@import "../../styles/variables.scss";
#sidebar {
  background-color: $wet-asphalt;
  width: 200px !important;
  height: 100%;
}
</style>

