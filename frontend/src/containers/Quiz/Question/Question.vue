<template>
    <v-card class="question col-md-8 offset-md-2">
        <h3>Question {{ questionIndex + 1 }}</h3>


        <vue-markdown v-if="!question.edit_mode">{{ questionDescription }}</vue-markdown>


       <v-textarea
          v-else
          hint="Question Description"
          auto-grow
          color="secondary"
          v-model="questionDescription"
        ></v-textarea>


  <v-data-table
    :headers="headers"
    :items="question.test_cases"
s
    no-data-text="No Test Cases"
    class="elevation-1"
  >
    <template slot="items" slot-scope="props">
      <td> <pre>{{ props.item.test_input }}</pre></td>
      <td><pre>{{ props.item.test_expected }}</pre></td>
    </template>
  </v-data-table>

  <div v-if="isTeacher() && question.edit_mode">
  <div class="split-fields">
    <v-textarea label="Test Case" color="secondary" v-model="testCaseContent" :error-messages="testCaseContentErrors"></v-textarea>
  </div>
  <div class="split-fields">
    <v-textarea label="Expected" color="secondary" v-model="testCaseExpected" :error-messages="testCaseExpectedErrors"></v-textarea>
  </div>

  </div>

  <v-btn flat v-if="isTeacher() && question.edit_mode" class="add-test-case" @click="addTestCase()">Add Test Case</v-btn>

  <div class="editor">
  </div>

  <div id="check-btns">
    <v-btn flat class="precheck-btn">Precheck</v-btn>

    <v-btn flat class="check-btn">Check</v-btn>

    <div style="clear: both;"></div>
  </div>

    </v-card>
</template>

<script>
import VueMarkdown from "vue-markdown";

export default {
  props: ["question", "questionIndex", "isTeacher"],
  components: {
    "vue-markdown": VueMarkdown
  },
  data() {
    return {
      headers: [
        {
          text: "Test Case",
          sortable: false,
          value: "testCase"
        },
        {
          text: "Expected",
          sortable: false,
          value: "expected"
        }
      ],
      questionDescription: this.question.question_description,
      testCaseContent: "",
      testCaseExpected: "",
      testCaseContentErrors: [],
      testCaseExpectedErrors: []
    };
  },
  mounted() {
    const editor = document.getElementsByClassName("editor")[
      this.questionIndex
    ];

    window.ace.edit(editor);
  },
  methods: {
    // Resets and checks for errors, and emits new-test-case events if no errors
    addTestCase() {
      this.testCaseContentErrors = [];
      this.testCaseExpectedErrors = [];

      if (!this.testCaseContent) {
        this.testCaseContentErrors.push("Field Required");
      }
      if (!this.testCaseExpected) {
        this.testCaseExpectedErrors.push("Field Required");
      }

      if (
        this.testCaseContentErrors.length ||
        this.testCaseExpectedErrors.length
      )
        return;

      this.testCaseContent = "";
      this.testCaseExpected = "";

      this.$emit("new-test-case", {
        testCaseContent: this.testCaseContent,
        testCaseExpected: this.testCaseExpected,
        questionIndex: this.questionIndex
      });
    }
  },
  watch: {
    questionDescription(newVal, oldVal) {
      this.$emit("alter-question", {
        questionDescription: this.questionDescription,
        questionIndex: this.questionIndex
      });
    }
  }
};
</script>


<style lang="scss">
@import "../../../styles/_variables.scss";
.question {
  margin-top: 30px;
  padding: 10px;
}

.question-right {
  background-color: rgba(46, 204, 113, 0.5);
}

.question-wrong {
  background-color: rgba(231, 76, 60, 0.5);
}

.add-test-case {
  background-color: $emerald !important;
  color: #fff !important;
  margin: 0 auto;
  display: block;
  margin-top: 10px;
}

.split-fields {
  width: 50%;
  float: left;
}

.editor {
  margin-top: 20px;
  height: 400px;
}

#check-btns {
  margin: 0 auto;
  width: 300px;
}

.precheck-btn {
  float: left;
  background-color: $emerald !important;
  color: #fff !important;
}

.check-btn {
  float: right;
  background-color: $emerald !important;
  color: #fff !important;
}
</style>

