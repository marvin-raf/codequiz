<template>
    <div>
        <v-card class="col-md-8 offset-md-2" id="course">
            <h1>{{courseName}}</h1>
        </v-card>
        <v-card class="col-md-8 offset-md-2" id="course">
            <v-list>
                <div v-for="(quiz, index) in quizzes.slice((page-1)*8, (page - 1) * 8 + 8)" v-bind:key="index">
                    <v-list-tile>
                        <v-list-title style="width: 100%;">
                            <div v-if="!quiz.input">
                                {{quiz.quiz_name}}
                                <v-btn @click="changeInput(index, true)" color="secondary" depressed style="float: right;">Edit</v-btn>
                            </div>
                            <div v-if="quiz.input">
                                <v-text-field color="secondary" maxlength="50" v-model="quizzes[index].quiz_name" style="float: left; width: 70%;"></v-text-field>
                                <v-btn @click="changeName(index, quiz.quiz_id, quiz.quiz_name)" color="secondary" depressed style="float: right;">Save</v-btn>
                            </div>
                        </v-list-title>
                        <v-list-content>
                        </v-list-content>
                        
                    </v-list-tile>
                    <v-divider v-if="index != quizzes.length - 1"></v-divider>
                </div>
                <v-pagination color="secondary" :length="Math.ceil(courses.length / 8)" id="course-pagination" v-model="page"></v-pagination>
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
      course: null,
      courseName: null,
      quizzes: null,
      quizName: null
    };
  },
  async mounted() {
    try {
      this.course = await helpers.getCourse(this.$route.params.id);
      this.courseName = this.course.course.course_name;
      this.quizzes = this.course.course.quizzes;
      console.log(this.course);
    } catch (e) {
      this.$router.push("/dashboard");
    }
  },
  methods: {
    async addQuiz() {
      try {
        const { quizId } = await helpers.addCourse(this.courseName);
        this.quizzes.push({
          quiz_name: this.quizName,
          quiz_id: quizId
        });
        this.quizName = null;
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
      this.$set(this.quizzes[index], "input", false);
    },
    changeInput: function(index, value) {
      this.$set(this.quizzes[index], "input", value);
    }
  }
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
#course-pagination {
  display: flex;
  justify-content: center;
}
</style>


