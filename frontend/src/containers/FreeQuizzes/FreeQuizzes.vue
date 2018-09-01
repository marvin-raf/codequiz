<template>
    <v-card class="col-sm-10 offset-sm-1" id="free-quizzes">
        <h1>Free Quizzes</h1>


    <v-progress-circular
      indeterminate
      color="secondary"
      id="free-quizzes-spinner"
      v-if="freeQuizzes === null"
    ></v-progress-circular>

    <v-else>
      <v-list>
      <!--.slice call gets only the quizzes we want on the specific page of the pagination-->
      <div v-for="(course, index) in freeQuizzes.slice((page-1)*8, (page - 1) * 8 + 8)" v-bind:key="index">
          <v-divider v-if="index === 0"></v-divider>
          <v-list-tile @click="">
              <v-list-title>
                <div class="quiz-name-language">
                <a @click="" href="#">{{ course.quiz_name }}</a>




                </div>

              </v-list-title>

              <v-list-content style="width: 100%;">
                <div class="quiz-short-description">

                  {{ course.quiz_short_desc }}



                </div>

                <i class="fab fa-python" id="quiz-icon"></i>





              </v-list-content>
                        
          </v-list-tile>
          <v-divider></v-divider>
      </div>
      <v-pagination color="secondary" :length="Math.ceil(freeQuizzes.length / 8)" id="free-quizzes-pagination" v-model="page"></v-pagination>
  </v-list>

    </v-else>

    </v-card>
</template>

<script>
import helpers from "./helpers";

export default {
  data() {
    return {
      freeQuizzes: null,
      page: 1 // Referring to the current page of pagination
    };
  },
  async mounted() {
    try {
      const freeQuizzes = await helpers.getFreeQuizzes();

      this.freeQuizzes = freeQuizzes;
    } catch (e) {
      console.log(e);
    }
  },
  methods: {}
};
</script>


<style lang="scss">
@import "../../styles/_mixins.scss";
@import "../../styles/_variables.scss";

#free-quizzes {
  background-color: #fff;
  @include card();

  h1 {
    text-align: center;
    color: $text-color;
  }

  a {
    text-decoration: none;
  }

  #free-quizzes-spinner {
    margin: 0 auto;
    display: block;
    margin-top: 50px;
  }

  .quiz-name-language {
    width: 100px;
    float: left;
  }

  .quiz-short-description {
    float: left;
  }

  #quiz-icon {
    font-size: 20px;
    color: $wet-asphalt;
    float: right;
  }

  #free-quizzes-pagination {
    display: flex;
    justify-content: center;
    bottom: 10px;
    position: absolute;
    margin-left: auto;
    margin-right: auto;
    left: 0;
    right: 0;
  }
}
</style>



