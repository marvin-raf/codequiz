<template>
  <div>

    <!--Modal that deletes questions and test cases-->

    <v-card class="question col-lg-10 offset-lg-1">

      <div v-if="isTeacher() && question.question_id">
        <DeleteQuestion v-on:question-deleted="questionDeleted" :quizId="$route.params.id" :questionId="question.question_id" />
        <br>
        <br>
      </div>

      <h3>Question {{ questionIndex + 1 }}
        <v-btn class="save-btn" v-if="question.edit_mode" color="secondary" @click="setEditMode()">Save</v-btn>

        <v-btn v-if="!question.edit_mode && isTeacher()" flat class="edit-btn" color="primary">
          <v-icon @click="setEditMode()" color="primary">edit</v-icon>
        </v-btn>
      </h3>

      <vue-markdown v-if="!question.edit_mode">{{ questionDescription }}</vue-markdown>

      <v-textarea v-else hint="Question Description" auto-grow color="secondary" v-model="questionDescription"></v-textarea>

      <TestCases :headers="headers" :testCases="question.test_cases" :isTeacher="isTeacher" :quizId="$route.params.id" :questionId="question.question_id" v-on:test-case-deleted="testCaseDeleted" />

      <v-btn flat v-if="isTeacher() && question.question_id" class="add-test-case" @click="$emit('open-test-case-modal', {questionId: question.question_id, questionIndex})">Add Test Case</v-btn>

      <codemirror class="editor" v-if="!question.edit_mode" v-model="editor" :options="cmOptions"></codemirror>

      <v-alert id="precheck-error" type="error" :value="precheckError.length">

        <div v-for="error in precheckError" v-bind:key="error">{{ error }}</div>
      </v-alert>

      <v-alert :value="precheckSuccess" id="precheck-success" type="success">
        Successful Precheck
      </v-alert>

      <v-data-table v-if="testCaseResults && testCaseResults.length" :headers="testCaseResultHeaders" :items="testCaseResults" no-data-text="" class="elevation-1" hide-actions>
        <template slot="items" slot-scope="props">
          <tr v-bind:class="{'question-right' : props.item.test_expected === props.item.output, 'question-wrong': props.item.test_expected !== props.item.output}">
            <td>
              <pre>{{ props.item.test_input }}</pre>
            </td>
            <td>
              <pre>{{ props.item.test_expected }}</pre>
            </td>
            <td>
              <pre>{{ props.item.output }}</pre>
            </td>
          </tr>
        </template>
      </v-data-table>

      <span v-if="testCaseResults && testCaseResults.length">
        Marks for this submission: {{ question.question_worth / 10}}
        <br />
        <span v-if="question.last_attempt_wrong">
          Total Negated: {{ question.total_negated / 10}}
        </span>
      </span>

      <div id="check-btns">
        <v-btn :flat="!hasFinished" class="precheck-btn" @click="precheck()" :loading="precheckLoading" v-if="!question.edit_mode" :disabled="hasFinished">Precheck</v-btn>

        <v-btn :flat="!hasFinished" class="check-btn" @click="check()" :loading="checkLoading" v-if="!question.edit_mode" :disabled="hasFinished">Check</v-btn>

        <div style="clear: both;"></div>

      </div>

    </v-card>
  </div>
</template>

<script>  






import VueMarkdown from "vue-markdown";
import studentStore from "../../../store/studentStore";
import teacherStore from "../../../store/teacherStore";

import DeleteQuestion from "./DeleteQuestion/DeleteQuestion";
import TestCases from "./TestCases/TestCases";

import helpers from "./helpers.js";

export default {
  props: ["question", "questionIndex", "isTeacher", "hasFinished"],
  components: {
    "vue-markdown": VueMarkdown,
    DeleteQuestion,
    TestCases
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
        },
        {
          text: "Actions",
          sortable: false,
          value: "actions",
          align: "right"
        }
      ],
      questionDescription: this.question.question_description,
      testCaseContent: "",
      testCaseExpected: "",
      testCaseError: false,
      editor: "",
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
      ],
      teacherStore: teacherStore.data,
      testCaseModal: false,
      testCaseIdEdit: null,
      testCaseDeleteId: null,
      testCaseDeleteIndex: null,
      cmOptions: {
        // codemirror options
        tabSize: 4,
        lineNumbers: true,
        indentUnit: 4,
        line: true,
        mode: "python",
        theme: "idea",
      }
    };
  },
  mounted() {
    this.testCaseResults = this.question.test_case_results;
 },
  methods: {
    async precheck() {
      // Reset success/error messages and spinner
      this.precheckError = [];
      this.precheckLoading = true;
      this.precheckSuccess = false;

      try {
        const output = await helpers.precheck(
          this.$route.params.id,
          this.question.question_id,
          this.editor,
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
        const json = await helpers.check(
          this.$route.params.id,
          this.question.question_id,
          this.editor
        );

        this.testCaseResults = json.results;
        
        this.checkLoading = false;

        this.$emit("update-question-worth", {
          questionIndex: this.questionIndex,
          questionWorth: json.question_worth,
          totalNegated: json.total_negated,
          lastAttemptWrong: json.last_attempt_wrong
        });
      } catch (e) {
        this.checkLoading = false;
      }
    },
    async setEditMode() {
      if (this.question.edit_mode) {
        try {
          if (this.question.question_id) { // If the question has been made, then edit it
            await helpers.updateQuestion(this.question);
            this.$emit("toggle-edit-question", {
              questionIndex: this.questionIndex
            });
          } else { // If question is not made, then make it
            console.log("Did I make it here");
            const questionId = await helpers.addQuestion(this.questionDescription, this.$route.params.id);

            this.$emit("save-question", {
              questionIndex: this.questionIndex,
              questionId
            });
          }
         } catch (e) {
           console.log(e);
         }
      } else {
        this.$emit("toggle-edit-question", {
          questionIndex: this.questionIndex
        });
      }
    },
    async deleteQuestion() {
      try {
        const quizId = this.$route.params.id;
        const questionId = this.question.question_id;
        await helpers.deleteQuestion(this.$route.params.id, questionId);
      } catch (e) {
        console.log(e);
      }

      this.deleteModal = false;

      this.$emit("delete-question", {
        questionIndex: this.questionIndex
      });
    },
    async deleteTestCase() {
      try {
        const quizId = this.$route.params.id;
        const questionId = this.question.question_id;
        const testId = this.testCaseDeleteId;
        await helpers.deleteTestCase(quizId, questionId, testId);

        
        this.$emit("delete-test-case", {
          questionIndex: this.questionIndex,
          testCaseIndex: this.testCaseDeleteIndex
        });
      } catch (e) {
        console.log(e);
      }

    },
    questionDeleted() {
      this.$emit("question-deleted", this.questionIndex); 
    },
    testCaseDeleted(testCaseIndex) {
      this.$emit("test-case-deleted", {
        testCaseIndex,
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

.wet-asphalt {
  background-color: $wet-asphalt;
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

.delete-btn {
  float: right;
  background-color: #e74c3c !important;
  color: #fff !important;
}

#precheck-error {
  background-color: rgba(231, 76, 60, 0.7) !important;
}

#precheck-success {
  background-color: rgba(46, 204, 113, 0.7) !important;
}

.delete-test-case-btn {
  cursor: pointer;

  &:hover {
    color: #e74c3c !important;
  }
}

.edit-test-case-btn {
  cursor: pointer;

  &:hover {
    color: $emerald !important;
  }
}

.edit-btn {
  width: 50px !important;
  min-width: 50px !important;
}

.save-btn {
  width: 50px !important;
  min-width: 50px !important;
}

.editor {
  margin-top: 10px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 2px;
}
</style>

