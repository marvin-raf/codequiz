<template>
    <div>
    <v-card class="col-md-8 offset-md-2" id="quiz">
        <h1 v-if="quizName">{{ quizName }}</h1>

    </v-card>

        <Question
        v-for="(question, index) in questions"
        :question="question"
        :questionIndex="index"
        v-bind:key="question.quiz_id"
        v-on:alter-question="alterDescription"
        v-on:new-test-case="addTestCase"
        >

        </Question>

        <v-btn flat id="new-question" @click="addQuestion()"><v-icon v-if="!addingQuestion">add</v-icon><span v-else>Save</span></v-btn>

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
      questions: null,
      addingQuestion: false
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
  },
  methods: {
    async addQuestion() {
      if (!this.addingQuestion) {
        this.questions.push({
          question_description: "",
          edit_mode: true,
          test_cases: []
        });

        this.addingQuestion = true;
        return;
      }

      const question = this.questions[this.questions.length - 1];

      try {
        await helpers.addQuestion(question);
      } catch (e) {
        console.log(e);
      }

      question.edit_mode = false;
      this.addingQuestion = false;
    },
    alterDescription(question) {
      this.questions[question.questionIndex].question_description =
        question.questionDescription;
    },
    addTestCase(testCase) {
      this.questions[testCase.questionIndex].test_cases.push({
        test_input: testCase.testCaseContent,
        test_expected: testCase.testCaseExpected
      });
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



