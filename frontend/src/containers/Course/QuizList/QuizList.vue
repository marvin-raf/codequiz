<template>
    <v-card class="col-md-8 offset-md-2" id="course">
        <v-list>
            <div v-for="(quiz, index) in quizzes.slice((page-1)*8, (page - 1) * 8 + 8)" v-bind:key="index">
                <v-list-tile style="height: 50px;">
                    <v-list-tile-title style="width: 100%; height: 45px;">
                        <div>
                            <a @click="$router.push('/quizzes/' + quiz.quiz_id)"> {{quiz.quiz_name}} </a>

                            <v-btn v-if="!quiz.input" @click="setupEdit(index)" flat style="min-width: 50px; width: 50px; float: right;">
                                <v-icon>edit</v-icon>
                            </v-btn>
                            <br>
                            <div style="font-size: 14px; color: grey;">{{convert(quiz.quiz_start_date)}} - {{convert(quiz.quiz_end_date)}}</div>
                        </div>

                    </v-list-tile-title>
                    <v-list-tile-content>
                    </v-list-tile-content>

                </v-list-tile>
                <v-divider v-if="index != quizzes.length - 1"></v-divider>
            </div>
            <v-pagination color="secondary" :length="Math.ceil(quizzes.length / 8)" id="course-pagination" v-model="page"></v-pagination>
        </v-list>
    </v-card>
</template>

<script>
import helpers from "./helpers";
export default {
  props: ["quizzes", "setupEdit", "convert"],
  data() {
    return {
      page: 1,
    };
  },
  async mounted() {},
  methods: {},
};
</script>

<style lang="scss">
@import "../../../styles/_mixins.scss";
@import "../../../styles/_variables.scss";
#course {
  background-color: #fff;
  h1 {
    text-align: center;
    color: $text-color;
  }
  padding-top: 20px;
  margin-top: 20px;
  padding-bottom: 20px;
  overflow: hidden;
}
#course-pagination {
  display: flex;
  justify-content: center;
}
</style>