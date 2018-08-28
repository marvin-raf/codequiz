<template>
    <div>
        <v-card class="col-md-8 offset-md-2" id="courses">
            <h1>Courses</h1>
            <v-text-field label="Course Name" v-model="courseName" color="secondary" maxlength="50" id="course-name" style="float: left; width: 70%"></v-text-field>
            <div id="create-box">
                <v-btn id="create-btn" color="secondary" @click="addCourse()" depressed :disabled="courseName ? false : true" style="float: right;">Create</v-btn> 
            </div>
        </v-card>
        <v-card class="col-md-8 offset-md-2" id="courses">
            <v-list>
                <div v-for="(course, index) in courses.slice((page-1)*8, (page - 1) * 8 + 8)" v-bind:key="index">
                    <v-list-tile>
                        <v-list-title style="width: 100%;">
                            <div v-if="!course.input">
                                <a @click="$router.push('/courses/' + course.course_id)"> {{course.course_name}} </a>
                                <v-btn @click="changeInput(index, true)" color="secondary" depressed style="float: right;">Edit</v-btn>
                            </div>
                            <div v-if="course.input">
                                <v-text-field color="secondary" maxlength="50" v-model="courses[index].course_name" style="float: left; width: 70%;"></v-text-field>
                                <v-btn @click="changeName(index, course.course_id, course.course_name)" color="secondary" depressed style="float: right;">Save</v-btn>
                            </div>
                        </v-list-title>
                        <v-list-content>
                        </v-list-content>
                        
                    </v-list-tile>
                    <v-divider v-if="index != courses.length - 1"></v-divider>
                </div>
                <v-pagination color="secondary" :length="Math.ceil(courses.length / 8)" id="courses-pagination" v-model="page"></v-pagination>
            </v-list>
            
        </v-card>

       
       
    </div>
</template>

<script>
import helpers from "./helpers";

import teacherStore from "../../store/teacherStore.js";
import studentStore from "../../store/studentStore.js";
export default {
  data() {
    return {
      courses: [],
      currentCourses: [],
      courseName: null,
      page: 1
    };
  },
  async mounted() {
    try {
      const { courses } = await helpers.getCourses();
      this.courses = courses;
      for (let i = 0; i < this.courses.length; i++) {
        //this.courses[i].input = false;
      }
    } catch (e) {
      console.log(e);
      this.$router.push("/dashboard");
    }
  },
  methods: {
    async addCourse() {
      try {
        const { courseId } = await helpers.addCourse(this.courseName);
        this.courses.push({
          course_name: this.courseName,
          course_id: courseId
        });
        this.courseName = null;
      } catch (e) {
        console.log(e);
      }
    },
    async changeName(index, id, name) {
      try {
        await helpers.changeName(id, name);
      } catch (e) {
        console.log(e);
      }
      this.$set(this.courses[index], "input", false);
    },
    changeInput: function(index, value) {
      this.$set(this.courses[index], "input", value);
    }
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
  overflow: hidden;
}

#courses-pagination {
  display: flex;
  justify-content: center;
}
</style>


