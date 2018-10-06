<template>
  <div>
    <TestCaseModal :quizId="$route.params.id" :testCaseModal="testCaseModal" :testCaseModalData="testCaseModalData" v-on:new-test-case="addTestCase" v-on:close-test-case-modal="testCaseModal = false"></TestCaseModal>

    <v-card class="col-lg-10 offset-lg-1" id="quiz">
      <h1 v-if="quizName">{{ quizName }}</h1>

      <!-- <DateTime v-if="quizName && !isLoggedIn()" :startDate="startDate" :startTime="startTime" :endDate="endDate" :endTime="endTime" :editDateTime="editDateTime" v-on:save-date-time="saveDateTime" v-on:toggle-edit-date-time="toggleDateTime" /> -->

    </v-card>

    <Question v-for="(question, index) in questions" :question="question" :questionIndex="index" :isTeacher="isTeacher" :hasFinished="hasFinished" v-bind:key="question.quiz_id" v-on:alter-question="alterDescription" v-on:update-question-worth="updateQuestionWorth" v-on:toggle-edit-question="toggleEditQuestion" v-on:delete-question="deleteQuestion" v-on:open-test-case-modal="openTestCaseModal" v-on:delete-test-case="deleteTestCase" v-on:save-question="saveQuestion">

    </Question>

    <v-btn flat id="new-question" @click="addQuestion()" v-if="isTeacher()">
      <v-icon>add</v-icon>
    </v-btn>

  </div>
</template>

<script>
import helpers from "./helpers";

import teacherStore from "../../store/teacherStore.js";
import studentStore from "../../store/studentStore.js";
import Question from "./Question/Question.vue";
import DateTime from "./DateTime/DateTime.vue";
import TestCaseModal from "./TestCaseModal/TestCaseModal.vue";

export default {
  components: {
    Question,
    DateTime,
    TestCaseModal
  },
  props: ["isInstance"],
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
      endTime: null,
      testCaseModal: false,
      testCaseModalData: null,
      qcCourseId: null,
      quizTeacherId: null,
      hasFinished: false 
    };
  },
  async mounted() {
    try {
      const {
        quizName,
        questions,
        qcStartDate,
        qcEndDate,
        qcCourseId,
        quizTeacherId 
      } = await helpers.getQuizData(this.$route.params.id, this.isInstance);

      // If student is logged in, and they aren't doing a free quiz, check times
      if (studentStore.data.studentId && qcCourseId) {
        const currentTime = Date.now();
        
        if (currentTime > qcEndDate) {
          console.log("This quiz has finished");
          this.hasFinished = true;
        } else {
          this.hasFinished = false; 
        }
        }

      // Parsing timestamps into date and times
      const startDateTime = helpers.getDateTime(qcStartDate);
      const endDateTime = helpers.getDateTime(qcEndDate);

      this.startDate = startDateTime.date;
      this.startTime = startDateTime.time;

      this.endDate = endDateTime.date;
      this.endTime = endDateTime.time;

      this.qcCourseId = qcCourseId;
      this.quizTeacherId = quizTeacherId;
      

      if (!this.startDate) {
        this.editDateTime = true;
      }

      this.quizName = quizName;
      this.questions = questions;

    } catch (e) {
      console.log(e);
      this.$router.push("/dashboard");
    }
  },
  methods: {
    async addQuestion() {
        this.questions.push({
          question_quiz_id: this.$route.params.id,
          question_description: "",
          edit_mode: true,
          test_cases: []
        });
    },
    alterDescription(question) {
      this.questions[question.questionIndex].question_description =
        question.questionDescription;
    },
    addTestCase(testCase) {
      this.questions[testCase.testCaseModalData.questionIndex].test_cases.push({
        test_id: testCase.testId,
        test_input: testCase.testCaseContent,
        test_expected: testCase.testCaseExpected
      });

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
      // Check if teacher is admin and on a free quiz or if teacher is admin on their own quiz
      return teacherStore.data.teacherId && ((!this.qcCourseId && teacherStore.data.teacherIsAdmin) ||
             (teacherStore.data.teacherId === this.quizTeacherId))
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
    },
    openTestCaseModal(obj) {
      this.testCaseModalData = obj;
      this.testCaseModal = true;
    },
    deleteTestCase(obj) {
      this.questions[obj.questionIndex].test_cases.splice(obj.testCaseIndex, 1);
    },
    saveQuestion(obj) {
      const question = this.questions[obj.questionIndex];
      
      question.edit_mode = false;
      question.question_id = obj.questionId
    },
  }
};
</script>

<style lang="scss">
@import "../../styles/_mixins.scss";
@import "../../styles/_variables.scss";
#quiz {
  @include dark-header();
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



