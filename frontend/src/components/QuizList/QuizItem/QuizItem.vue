<template>
    <v-list-tile @click="$router.push(`/quizzes/${quiz.qc_id}`)">
        <span>
            <div class="quiz-name-language">

                <a @click="$router.push(`/quizzes/${quiz.qc_id}`)" href="#">{{ quiz.quiz_name }}</a>

            </div>

        </span>

        <v-list-tile-content style="width: 100%;">
            <div class="quiz-short-description">

                {{ quiz.quiz_short_desc }}

            </div>

        </v-list-tile-content>
        <font-awesome-icon :icon="['fab', 'python']" id="quiz-icon" />

    </v-list-tile>
</template>

<script>
export default {
    props: ["quiz"]
}
</script>

<style lang="scss">
a {
  text-decoration: none;
}

.quiz-name-language {
  width: 100px;
  float: left;
}

.quiz-short-description {
  float: left;
}
</style>


