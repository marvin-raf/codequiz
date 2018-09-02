<template>
    <div>

    <v-card class="col-md-8 offset-md-2" id="quiz">
        <h1 v-if="quizName">{{ quizName }}</h1>

        <DateTime 
          v-if="quizName && !isLoggedIn()"
          :startDate="startDate" 
          :startTime="startTime"
          :endDate="endDate"
          :endTime="endTime"
          :editDateTime="editDateTime"
          v-on:save-date-time="saveDateTime"
          v-on:toggle-edit-date-time="toggleDateTime"
          
          
        />


    </v-card>

        <Question
        v-for="(question, index) in questions"
        :question="question"
        :questionIndex="index"
        :isTeacher="isTeacher"
        v-bind:key="question.quiz_id"
        v-on:alter-question="alterDescription"
        v-on:new-test-case="addTestCase"
        v-on:update-question-worth="updateQuestionWorth"
        v-on:toggle-edit-question="toggleEditQuestion"
        v-on:delete-question="deleteQuestion"
        >

        </Question>

        <v-btn flat id="new-question" @click="addQuestion()" v-if="isTeacher()"><v-icon v-if="!addingQuestion">add</v-icon><span v-else>Save</span></v-btn>

        </div>
</template>

<script>
import helpers from "./helpers";

import teacherStore from "../../store/teacherStore.js";
import studentStore from "../../store/studentStore.js";
import Question from "./Question/Question.vue";
import DateTime from "./DateTime/DateTime.vue";

export default {
  components: {
    Question,
    DateTime
  },
  data() {
    return {
      teacherStore: teacherStore.data,
      studentStore: studentStore.data,
      quizName: null,
      questions: null,
      addingQuestion: false,
      editDateTime: false,
      startDate: null,
      startTime: null,
      endDate: null,
      endTime: null
    };
  },
  async mounted() {
    try {
      const {
        quizName,
        questions,
        quizStartDate,
        quizEndDate
      } = await helpers.getQuizData(this.$route.params.id);

      // Parsing timestamps into date and times
      const startDateTime = helpers.getDateTime(quizStartDate);
      const endDateTime = helpers.getDateTime(quizEndDate);

      this.startDate = startDateTime.date;
      this.startTime = startDateTime.time;

      this.endDate = endDateTime.date;
      this.endTime = endDateTime.time;

      if (!this.startDate) {
        this.editDateTime = true;
      }

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
        await helpers.addQuestion(question, this.$route.params.id);
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
      console.log("Test case added");
      console.log(testCase.testCaseContent);
      console.log(testCase.testCaseExpected);
      this.questions[testCase.questionIndex].test_cases.push({
        test_input: testCase.testCaseContent,
        test_expected: testCase.testCaseExpected
      });

      console.log(this.questions[testCase.questionIndex]);
    },
    saveDateTime(dateTimes) {
      const { startDate, startTime, endDate, endTime } = dateTimes;

      this.startDate = startDate;
      this.startTime = startTime;
      this.endDate = endDate;
      this.endTime = endTime;
      this.toggleDateTime();
    },
    toggleDateTime() {
      this.editDateTime = !this.editDateTime;
    },
    isTeacher() {
      return teacherStore.data.teacherId;
    },
    isLoggedIn() {
      return teacherStore.data.teacherId || studentStore.data.studentId;
    },
    updateQuestionWorth(obj) {
      this.questions[obj.questionIndex].question_worth = obj.questionWorth;
      this.questions[obj.questionIndex].total_negated = obj.totalNegated;
      this.questions[obj.questionIndex].last_attempt_wrong =
        obj.lastAttemptWrong;
    },
    toggleEditQuestion(obj) {
      this.$set(
        this.questions[obj.questionIndex],
        "edit_mode",
        !this.questions[obj.questionIndex].edit_mode
      );
    },
    deleteQuestion(obj) {
      this.questions.splice(obj.questionIndex, 1);
    }
  }
};
</script>

<style lang="scss">
@import "../../styles/_mixins.scss";
@import "../../styles/_variables.scss";
#quiz {
  background-color: $wet-asphalt;

  h1 {
    text-align: center;
    color: #fff;
  }
  padding-top: 20px;
  margin-top: 20px;
  padding-bottom: 20px;
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
  margin-bottom: 20px;
}

.split-fields {
  width: 50%;
  float: left;
}

#to span {
  text-align: center;
}
</style>



