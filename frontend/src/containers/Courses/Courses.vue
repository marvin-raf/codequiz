<template>
    <div>
        <v-card class="col-md-8 offset-md-2" id="courses">
            <h1>Courses</h1>
            <v-text-field label="Course Name" v-model="courseName" color="secondary"></v-text-field>
            <v-btn color="secondary" depressed>Create</v-btn> 
        </v-card>
        <v-card class="col-md-8 offset-md-2" id="courses">
            
        </v-card>
    </div>
</template>

<script>
import teacherStore from "../../store/teacherStore.js";
import studentStore from "../../store/studentStore.js";
export default {
  data() {
    return {
      courseName: null
    };
  }
};
</script>

<style lang="scss">
@import "../../styles/_mixins.scss";
@import "../../styles/_variables.scss";
#courses {
  background-color: #fff;
  h1 {
    text-align: center;
    color: $text-color;
  }
  padding-top: 20px;
  margin-top: 20px;
  padding-bottom: 20px;
}
</style>


