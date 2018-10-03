<template>
    <v-list>
        <!--.slice call gets only the quizzes we want on the specific page of the pagination-->
        <div v-for="(quiz, index) in getQuizzes()" v-bind:key="index">
            <v-divider v-if="index === 0"></v-divider>
            <QuizItem :quiz="quiz" />
            <v-divider></v-divider>
        </div>
    </v-list>
</template>

<script>
          
import QuizItem from "./QuizItem/QuizItem";


export default {
    components: {
        QuizItem
    },
    props: ["quizzes", "page", "perPage"],
    data() {
        return {

        };
    },
    methods: {
        // Gets index of page to slice from
        getQuizzes() {
            return this.quizzes.slice((this.page - 1) * this.perPage, ((this.page - 1) * this.perPage) + this.perPage);
        }
    }
}</script>

