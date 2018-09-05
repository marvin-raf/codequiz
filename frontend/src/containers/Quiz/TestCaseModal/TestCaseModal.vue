<template>
    <v-dialog v-model="testCaseModal" persistent width="800">

        <v-card>
            <v-card-title class="headline justify-center wet-asphalt" primary-title>
                <span style="color: #fff;">Add Test Case</span>
            </v-card-title>

            <v-divider></v-divider>

            <div style="padding: 10px;">
                <v-alert :value="testCaseError" type="error">
                    {{ testCaseError }}
                </v-alert>

                <div class="split-fields">
                    <h3 style="text-align: center;">Test Case</h3>
                </div>

                <div class="split-fields">
                    <h3 style="text-align: center;">Expected Result</h3>
                </div>
                <div class="split-fields">
                    <div id="test-case-editor"></div>
                </div>
                <div class="split-fields">
                    <div id="expected-editor"></div>
                </div>

            </div>

            <v-card-actions style="width: 200px;margin: 0 auto;">
                <v-btn color="primary" flat @click="$emit('close-test-case-modal')">
                    Go Back
                </v-btn>

                <v-btn color="secondary" flat @click="addTestCase();">
                    Create
                </v-btn>

            </v-card-actions>
        </v-card>
    </v-dialog>

</template>



<script>
import helpers from "./helpers";


export default {
    props: ["quizId", "testCaseModal", "testCaseModalData"],
    data() {
        return {
            testCaseEditor: null,
            expectedEditor: null, 
            testCaseError:  false,
            modal: false
        };
    },
    mounted() {
        
      const testCaseEditorNode = document.getElementById(
        "test-case-editor"
        );

    const expectedEditorNode = document.getElementById(
      "expected-editor"
    );

    const testCaseEditor = window.ace.edit(testCaseEditorNode);
    const expectedEditor = window.ace.edit(expectedEditorNode);

    testCaseEditor.setOptions({
      useSoftTabs: true
    });

    expectedEditor.setOptions({
      useSoftTabs: true
    });

    testCaseEditor.getSession().setMode("ace/mode/python");

    this.testCaseEditor = testCaseEditor;
    this.expectedEditor = expectedEditor;
    },
    methods: {
        async addTestCase() {
        this.testCaseError = false;
        if (!this.testCaseEditor.getValue() || !this.expectedEditor.getValue()) {
            this.testCaseError = "Test input and Test expected fields required";
        }

        if (this.testCaseError) return;

        try {
            const quizId = this.quizId;
            const questionId = this.testCaseModalData.questionId;
            const testInput = this.testCaseEditor.getValue();
            const testExpected = this.expectedEditor.getValue();
            await helpers.addTestCase(quizId, questionId, testInput, testExpected);

            this.$emit("new-test-case", {
            testCaseContent: this.testCaseEditor.getValue(),
            testCaseExpected: this.expectedEditor.getValue(),
            testCaseModalData: this.testCaseModalData
            });

            this.$emit("close-test-case-modal");
        } catch (e) {
            this.testCaseError = "Server Error";
        }
            
        }
    }
}
</script>

<style lang="scss">
#test-case-editor {
  height: 400px;
}

#expected-editor {
  height: 400px;
}
</style>
