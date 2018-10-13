<template>
    <v-dialog :value="testCaseModal" persistent width="800">

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
                    <codemirror v-model="testCaseEditor" ref="testCaseEditor" :options="cmOptions"></codemirror>
                </div>
                <div class="split-fields">
                    <codemirror v-model="expectedEditor" ref="expectedEditor" :options="cmOptions"></codemirror>
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
            testCaseEditor: "",
            expectedEditor: "", 
            testCaseError:  false,
            modal: false,
            cmOptions: {
                // codemirror options
                tabSize: 4,
                indentUnit: 4,
                line: true,
                mode: "python",
                theme: "idea",
            }
        };
    },
    methods: {
        async addTestCase() {
        this.testCaseError = false;
        if (!this.testCaseEditor || !this.expectedEditor) {
            this.testCaseError = "Test input and Test expected fields required";
        }

        if (this.testCaseError) return;

        try {
            const quizId = this.quizId;
            const questionId = this.testCaseModalData.questionId;
            const testInput = this.testCaseEditor;
            const testExpected = this.expectedEditor;
            const testId = await helpers.addTestCase(quizId, questionId, testInput, testExpected);

            this.$emit("new-test-case", {
                testId,
                testCaseContent: this.testCaseEditor,
                testCaseExpected: this.expectedEditor,
                testCaseModalData: this.testCaseModalData
            });

            this.$emit("close-test-case-modal");
        } catch (e) {
            this.testCaseError = "Server Error";
        }
            
        }
    },
    watch: {
        testCaseModal(val) {
            if (val === true) {
                this.$refs.testCaseEditor.refresh();
                this.$refs.expectedEditor.refresh();
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

.split-fields {
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  border-right: 1px solid rgba(0, 0, 0, 0.1);
}
</style>
