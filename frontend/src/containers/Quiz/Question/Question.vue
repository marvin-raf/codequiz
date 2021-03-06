<template>
  <v-card class="question col-lg-10 offset-lg-1">

    <div class="text-xs-center">
      <v-dialog v-model="deleteModal" width="500">

        <v-card>
          <v-card-title class="headline red lighten-1 justify-center" primary-title>
            <span style="color: #fff;">Are you sure?</span>
          </v-card-title>

          <v-divider></v-divider>

          <v-card-actions style="width: 200px;margin: 0 auto;">
            <v-btn color="primary" flat @click="deleteModal = false">
              Go Back
            </v-btn>

            <v-btn color="red lighten-1" flat @click="deleteQuestion();">
              Delete
            </v-btn>

          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog v-model="deleteTestCaseModal" width="500">

        <v-card>
          <v-card-title class="headline red lighten-1 justify-center" primary-title>
            <span style="color: #fff;">Are you sure?</span>
          </v-card-title>

          <v-divider></v-divider>

          <v-card-actions style="width: 200px;margin: 0 auto;">
            <v-btn color="primary" flat @click="deleteTestCaseModal = false">
              Go Back
            </v-btn>

            <v-btn color="red lighten-1" flat @click="deleteTestCase();">
              Delete
            </v-btn>

          </v-card-actions>
        </v-card>
      </v-dialog>

    </div>

    <div v-if="isTeacher()">
      <v-btn flat class="delete-btn" @click="deleteModal = true;">
        <v-icon>delete</v-icon>
      </v-btn>
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

      <v-data-table :headers="headers" :items="question.test_cases" no-data-text="No Test Cases" class="elevation-1" hide-actions>
        <template slot="items" slot-scope="props">
          <td>
            <pre>{{ props.item.test_input }}</pre>
          </td>
          <td>
            <pre>{{ props.item.test_expected }}</pre>
          </td>
          <td class="text-xs-right">
            <v-icon v-if="isTeacher()" class="edit-test-case-btn" color="primary" @click="testCaseIdEdit = props.item.test_id; testCaseModal = true;">
              edit
            </v-icon>
            <v-icon v-if="isTeacher()" class="delete-test-case-btn" color="primary" @click="testCaseDeleteId = props.item.test_id; testCaseDeleteIndex = props.index; deleteTestCaseModal = true;">
              delete
            </v-icon>
          </td>
        </template>
      </v-data-table>

      <v-btn flat v-if="isTeacher()" class="add-test-case" @click="$emit('open-test-case-modal', {questionId: question.question_id, questionIndex})">Add Test Case</v-btn>

      <div class="editor" v-if="!question.edit_mode">
      </div>

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
</template>

<script>  
import VueMarkdown from "vue-markdown";
import studentStore from "../../../store/studentStore";
import teacherStore from "../../../store/teacherStore";

import helpers from "./helpers.js";

export default {
  props: ["question", "questionIndex", "isTeacher", "hasFinished"],
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
      ],
      deleteModal: false,
      teacherStore: teacherStore.data,
      testCaseModal: false,
      testCaseIdEdit: null,
      testCaseDeleteId: null,
      testCaseDeleteIndex: null,
      deleteTestCaseModal: false,
    };
  },
  mounted() {
    this.testCaseResults = this.question.test_case_results;

    // Setup all the ace editors
    const editorNode = document.getElementsByClassName("editor")[
      this.questionIndex
    ];

    const testCaseEditorNode = document.getElementsByClassName(
      "test-case-editor"
    )[this.questionIndex];

    const expectedEditorNode = document.getElementsByClassName(
      "expected-editor"
    )[this.questionIndex];


    const editor = window.ace.edit(editorNode);

    editor.setOptions({
      useSoftTabs: true
    });

    editor.getSession().setMode("ace/mode/python");

    this.editor = editor;
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
        const json = await helpers.check(
          this.$route.params.id,
          this.question.question_id,
          this.editor.getValue()
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

        this.deleteTestCaseModal = false;
        
        this.$emit("delete-test-case", {
          questionIndex: this.questionIndex,
          testCaseIndex: this.testCaseDeleteIndex
        });
      } catch (e) {
        console.log(e);
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
</style>

