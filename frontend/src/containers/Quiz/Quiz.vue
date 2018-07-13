<template>
    <div>
    <v-card class="col-md-8 offset-md-2" id="quiz">
        <h1 v-if="quizName">{{ quizName }}</h1>

    </v-card>

        <Question v-for="question in questions" :question="question" v-bind:key="question.quiz_id" >

        </Question>

        <v-btn flat id="new-question"><v-icon>add</v-icon></v-btn>

        </div>
</template>

<script>
import helpers from "./helpers";

import teacherStore from "../../store/teacherStore.js";
import studentStore from "../../store/studentStore.js";
import Question from "./Question/Question.vue";

export default {
  components: {
    Question
  },
  data() {
    return {
      teacherStore: teacherStore.data,
      studentStore: studentStore.data,
      quizName: null,
      questions: null
    };
  },
  async mounted() {
    try {
      const { quizName, questions } = await helpers.getQuizData(
        this.$route.params.id
      );

      this.quizName = quizName;
      this.questions = questions;
    } catch (e) {
      this.$router.push("/dashboard");
    }
  }
};
</script>

<style lang="scss">
@import "../../styles/_mixins.scss";
@import "../../styles/_variables.scss";
#quiz {
  background-color: #fff;
  h1 {
    line-height: 100px;
    text-align: center;
    color: $text-color;
  }

  height: 200px !important;
  margin-top: 20px;
  max-height: 100px;
}

#sign-in-btn {
  display: block;
  margin: 0 auto;
}

#new-question {
  background-color: $emerald !important;
  color: #fff;
  margin: 0 auto;
  display: block;
  margin-top: 30px;
}
</style>



