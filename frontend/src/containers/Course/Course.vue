<template>
    <div>
        <v-card class="col-md-8 offset-md-2" id="course">
            <h1>{{course.course.course_name}}</h1>
        </v-card>
        <v-card class="col-md-8 offset-md-2" id="course">
        </v-card>  
    </div>
</template>

<script>
import helpers from "./helpers";

import teacherStore from "../../store/teacherStore.js";
import studentStore from "../../store/studentStore.js";
export default {
  data() {
    course: null;
  },
  async mounted() {
    try {
      this.course = await helpers.getCourse(this.$route.params.id);
    } catch (e) {
      this.$router.push("/dashboard");
    }
  },
  methods: {}
};
</script>

<style lang="scss">
@import "../../styles/_mixins.scss";
@import "../../styles/_variables.scss";
#course {
  background-color: #fff;
  h1 {
    text-align: center;
    color: $text-color;
  }
  padding-top: 20px;
  margin-top: 20px;
  padding-bottom: 20px;
  overflow: hidden;
}
</style>


