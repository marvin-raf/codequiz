<template>
  <v-navigation-drawer id="sidebar" dark permanent>
    <v-list>
      <v-list-tile>
        <v-list-tile-title>Quiz Server</v-list-tile-title>
      </v-list-tile>
      <v-list-tile v-if="checkShowItem(item)" v-for="item in appItems" :key="item.title" @click="$router.push(item.url)">
        <v-list-tile-action>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-tile-action>

        <v-list-tile-content>
          <v-list-tile-title>{{ item.title }}</v-list-tile-title>
        </v-list-tile-content>

      </v-list-tile>
      <v-divider></v-divider>
      <v-list-tile v-if="checkShowItem(item)" v-for="item in authItems" :key="item.title" @click="authClick(item)">
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
import studentStore from "../../store/studentStore.js";
import teacherStore from "../../store/teacherStore.js";

import helpers from "./helpers.js";

export default {
  data() {
    return {
      studentStore: studentStore.data,
      teacherStore: teacherStore.data,
      authItems: [
        {
          title: "About",
          url: "/about",
          icon: "info",
          signedIn: null,
          showForTeacher: true,
          showForStudent: true
        },
        {
          title: "Sign Up",
          url: "/signup",
          icon: "lock",
          signedIn: false,
          showForTeacher: true,
          showForStudent: true
        },
        {
          title: "Sign In",
          url: "/signin",
          icon: "lock",
          signedIn: false,
          showForTeacher: true,
          showForStudent: true
        },
        {
          title: "Sign Out",
          url: "/signout",
          icon: "lock",
          signedIn: true,
          showForTeacher: true,
          showForStudent: true
        }
      ],
      appItems: [
        {
          title: "Dashboard",
          url: "/dashboard",
          icon: "dashboard",
          signedIn: true,
          showForTeacher: true,
          showForStudent: true
        },
        {
          title: "Classes",
          url: "/classes",
          icon: "book",
          signedIn: true,
          showForTeacher: true,
          showForStudent: false
        },
        {
          title: "Courses",
          url: "/courses",
          icon: "folder",
          signedIn: true,
          showForTeacher: true,
          showForStudent: true
        },
        {
          title: "Free Quizzes",
          url: "/freequizzes",
          icon: "assignment",
          signedIn: null,
          showForTeacher: true,
          showForStudent: true
        }
      ]
    };
  },
  methods: {
    checkShowItem(item) {
      if (item.signedIn === null) return true;

      if (
        item.signedIn === false &&
        (!this.studentStore.studentId && !this.teacherStore.teacherId)
      )
        return true;

      if (item.signedIn === true) {
        if (item.showForTeacher && this.teacherStore.teacherId) return true;
        if (item.showForStudent && this.studentStore.studentId) return true;
      }

      return false;
    },
    async authClick(item) {
      if (item.url === "/signout") {
        try {
          await helpers.signOut();
          this.$router.push("/");
        } catch (e) {
          console.log(e);
        }
      } else {
        this.$router.push(item.url);
      }
    }
  }
};
</script>


<style lang="scss" scoped>
@import "../../styles/variables.scss";
#sidebar {
  background-color: $wet-asphalt;
  width: 200px !important;
  height: 100%;
  position: fixed;
}
</style>

