<template>
    <div>
        <DeleteModal :deleteModal="deleteTestCase.modal" :confirmEvent="deletingTestCase" :cancelEvent="() => {deleteTestCase = false}" />

        <v-data-table :headers="headers" :items="testCases" no-data-text="No Test Cases" class="elevation-1" hide-actions>
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
                    <v-icon v-if="isTeacher()" class="delete-test-case-btn" color="primary" @click="deleteTestCaseModal(props.item.test_id, props.index)">
                        delete
                    </v-icon>
                </td>
            </template>
        </v-data-table>
    </div>
</template>

<script>

import DeleteModal from "../../../../components/DeleteModal/DeleteModal"
import notificationStore from "../../../../store/notificationStore";


import helpers from "./helpers";

export default {
    components: {
        DeleteModal
    },
    props: ["quizId", "questionId", "headers", "testCases", "isTeacher"],
    data() {
        return {
            deleteTestCase: {
                modal: false,
                id: null,
                index: null
            }
            
        };
    },
    methods: {
        deleteTestCaseModal(testCaseId, testCaseIndex) {
            this.deleteTestCase.id = testCaseId;
            this.deleteTestCase.index = testCaseIndex;
            this.deleteTestCase.modal = true;
        },
        async deletingTestCase() {
            try {
                await helpers.deleteTestCase(this.quizId, this.questionId, this.deleteTestCase.id)
                this.$emit("test-case-deleted", this.deleteTestCase.index);
                this.deleteTestCase.modal = false;
                this.deleteTestCase.id = null;
                this.deleteTestCase.index = null;
                notificationStore.methods.showNotification({
                    text: "Test Case Deleted",
                    isError: false
                });
            } catch (e) {
                console.log(e);
            }
        }
    }
}
</script>

