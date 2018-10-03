<template>
    <div>
        <v-card class="col-lg-10 offset-lg-1" id="quiz-header">
            <h1>Quizzes</h1>
        </v-card>

        <v-card class="col-lg-10 offset-lg-1" id="quiz-content">
            <QuizList :quizzes="quizzes" :page="page" :perPage="PER_PAGE" />

            <v-pagination color="secondary" :length="Math.ceil(quizzes.length / PER_PAGE)" id="quizzes-pagination" v-model="page"></v-pagination>

        </v-card>
    </div>
</template>

<script>
import QuizList from "../../components/QuizList/QuizList";

import helpers from "./helpers";

export default {
    components: {
        QuizList
    },
    data() {
        return {
            quizzes: [],
            page: 1,
            PER_PAGE: 8
        };
    },
    async mounted() {
        const quizzes = await helpers.getQuizzes();
        console.log(quizzes);
        this.quizzes = quizzes;
    },
    methods: {
        
    }
}
</script>


<style lang="scss">
@import "../../styles/_mixins.scss";

#quiz-header {
  @include dark-header();
}

#quiz-content {
  margin-top: 20px;
}

#quizzes-pagination {
  display: flex;
  justify-content: center;
  bottom: 10px;
  margin-left: auto;
  margin-right: auto;
  left: 0;
  right: 0;
}
</style>



