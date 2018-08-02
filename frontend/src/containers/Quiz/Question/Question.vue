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
    no-data-text="No Test Cases"
    class="elevation-1"
    hide-actions
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

  <v-alert
    id="precheck-error" 
    type="error"
    :value="precheckError.length"
  >


  <div v-for="error in precheckError" v-bind:key="error">{{ error }}</div>
  </v-alert>

   <v-alert
      :value="precheckSuccess"
      id="precheck-success"
      type="success"
    >
      Successful Precheck
    </v-alert>

   <v-data-table
    v-if="testCaseResults"
    :headers="testCaseResultHeaders"
    :items="testCaseResults"
    no-data-text="No Test Cases"
    class="elevation-1"
    hide-actions
  >
    <template slot="items" slot-scope="props">
      <tr v-bind:class="{'question-right' : props.item.test_expected === props.item.output, 'question-wrong': props.item.test_expected !== props.item.output}">
      <td> <pre>{{ props.item.test_input }}</pre></td>
      <td><pre>{{ props.item.test_expected }}</pre></td>
      <td><pre>{{ props.item.output }}</pre></td>
      </tr>
    </template>
  </v-data-table>
 

    


  <div id="check-btns">
    <v-btn
      flat
      class="precheck-btn"
      @click="precheck()"
      :loading="precheckLoading"
      >Precheck</v-btn>

    <v-btn
      flat
      class="check-btn"
      @click="check()"
      :loading="checkLoading"
      >Check</v-btn>

    <div style="clear: both;"></div>
  </div>

    </v-card>
</template>

<script>
import VueMarkdown from "vue-markdown";

import helpers from "./helpers.js";

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
      testCaseExpectedErrors: [],
      editor: null,
      precheckError: [],
      precheckSuccess: false,
      precheckLoading: false,
      checkLoading: false,
      testCaseResults: null,
      testCaseResultHeaders: [
        {
          text: "Test Case",
          sortable: false,
          value: "testCase"
        },
        {
          text: "Expected",
          sortable: false,
          value: "expected"
        },
        {
          text: "Actual",
          sortable: false,
          value: "actual"
        }
      ]
    };
  },
  mounted() {
    const editorNode = document.getElementsByClassName("editor")[
      this.questionIndex
    ];

    const editor = window.ace.edit(editorNode);

    this.editor = editor;

    editor.setOptions({
      useSoftTabs: true
    });

    editor.getSession().setMode("ace/mode/python");
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
    },
    async precheck() {
      // Reset success/error messages and spinner
      this.precheckError = [];
      this.precheckLoading = true;
      this.precheckSuccess = false;

      try {
        const output = await helpers.precheck(
          this.$route.params.id,
          this.question.question_id,
          this.editor.getValue()
        );

        if (output !== "") {
          this.precheckError = output.split("E:").slice(1);
        } else {
          this.precheckSuccess = true;
        }

        this.precheckLoading = false;
      } catch (e) {
        console.log(e);
        this.precheckLoading = false;
      }
    },
    async check() {
      this.precheckError = [];
      this.precheckSuccess = false;
      this.checkLoading = true;

      try {
        const testCases = await helpers.check(
          this.$route.params.id,
          this.question.question_id,
          this.editor.getValue()
        );

        this.testCaseResults = testCases;

        this.checkLoading = false;
      } catch (e) {
        this.checkLoading = false;
      }
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

#precheck-error {
  background-color: rgba(231, 76, 60, 0.7) !important;
}

#precheck-success {
  background-color: rgba(46, 204, 113, 0.7) !important;
}
</style>

