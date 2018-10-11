<!--
DeleteQuestion is responsible for rendering the delete question button
along with the functionality of deleting a question.
-->


<template>
    <div>
        <v-btn flat class="delete-btn" @click="deleteQuestionModal = true">
            <v-icon>delete</v-icon>
        </v-btn>
        <DeleteModal :deleteModal="deleteQuestionModal" :confirmEvent="deleteQuestion" :cancelEvent="cancelEvent" />

    </div>
</template>

<script>
import DeleteModal from "../../../../components/DeleteModal/DeleteModal";

import helpers from "./helpers";


export default {
    components: {
        DeleteModal
    },
    props: ["quizId", "questionId"],
    data()  {
        return {
            deleteQuestionModal: false
        };
    },
    methods: {
       /*
         deleteQuestion deletes a question and tells Quiz to update the array
       */
       async deleteQuestion() {
           try {
                await helpers.deleteQuestion(this.quizId, this.questionId)
                this.deleteQuestion = false;
                this.$emit("question-deleted");
           } catch (e) {
               console.log(e);
               console.log("There was an error");
           }

       },
       cancelEvent() {
           this.deleteQuestionModal = false;
       }
    }
}
</script>

