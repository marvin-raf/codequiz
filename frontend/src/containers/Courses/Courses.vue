<template>
    <div>
        <AddCourse :courseName.sync="courseName" :addCourse="addCourse"></AddCourse>
        <CourseList :courses="courses" :changeName="changeName" :changeInput="changeInput"></CourseList>
    </div>
</template>

<script>
import helpers from "./helpers";

//Auth
import teacherStore from "../../store/teacherStore.js";
import studentStore from "../../store/studentStore.js";

//Components
import AddCourse from "./AddCourse/AddCourse.vue";
import CourseList from "./CourseList/CourseList.vue";

export default {
  components: {
    AddCourse,
    CourseList,
  },
  data() {
    return {
      courses: [],
      courseName: null,
    };
  },
  async mounted() {
    this.getCourses();
  },
  methods: {
    async getCourses() {
      try {
        const { courses } = await helpers.getCourses();
        this.courses = courses;
      } catch (e) {
        console.log(e);
        this.$router.push("/dashboard");
      }
    },

    async addCourse() {
      try {
        const course = await helpers.addCourse(this.courseName);
        this.courses.push({
          course_name: this.courseName,
          course_id: course.course_id,
        });
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
    },
  },
};
</script>




