<template>
  <v-card class="col-sm-10 offset-sm-1" id="free-quizzes">

    <v-card-title class="headline" id="new-quiz-header" primary-title>
      Free Quizzes
    </v-card-title>

    <v-progress-circular indeterminate color="secondary" id="free-quizzes-spinner" v-if="freeQuizzes === null"></v-progress-circular>

    <div v-else>
      <List :items="freeQuizzes" :page="page" :perPage="8" nameKey="qc_id" descriptionKey="quic_short_desc" :generateUrl="generateUrl" :icon="['fab', 'python']" />

      <v-btn color="secondary" id="new-free-quiz-btn" @click="newQuizDialog = true;" v-if="teacherStore.teacherIsAdmin">
        <v-icon>add</v-icon>
      </v-btn>

      <v-pagination color="secondary" :length="Math.ceil(freeQuizzes.length / 8)" id="free-quizzes-pagination" v-model="page"></v-pagination>

      <v-dialog v-model="newQuizDialog" width="600">

        <v-card>
          <v-card-title class="headline" id="new-quiz-header" primary-title>
            Create New Free Quiz
          </v-card-title>

          <v-card-text>

            <v-alert :value="createQuizError" type="error">
              There was an error creating the quiz
            </v-alert>

            <v-text-field type="text" label="Quiz Name" color="secondary" :error-messages="quizNameErrors" maxlength="30" v-model="newQuizName">

            </v-text-field>

            <v-select :items="languages" label="Quiz Language" item-value="language_id" item-text="language_name" :error-messages="quizLanguageErrors" v-model="newQuizLanguage"></v-select>

            <v-textarea name="input-7-1" label="Short Description" color="secondary" v-model="newShortDescription" maxlength="50" :error-messages="shortDescriptionErrors"></v-textarea>

          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="secondary" flat @click="createFreeQuiz()" :loading="newQuizLoading">
              Create
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

    </div>

  </v-card>
</template>

<script>
import helpers from "./helpers";
import teacherStore from "../../store/teacherStore";
import List from "../../components/List/List";

export default {
  components: {
    List
  },
  data() {
    return {
      freeQuizzes: [],
      page: 1, // Referring to the current page of pagination
      teacherStore: teacherStore.data,
      newQuizDialog: false,
      newQuizName: "",
      newQuizLanguage: null,
      newShortDescription: "",
      languages: [],
      quizNameErrors: [],
      quizLanguageErrors: [],
      shortDescriptionErrors: [],
      newQuizLoading: false,
      createQuizError: false
    };
  },
  async mounted() {
    try {
      const freeQuizzes = await helpers.getFreeQuizzes();
      console.log(freeQuizzes);
      this.freeQuizzes = freeQuizzes;

      // If user is an admin, then get all languages
      if (teacherStore.data.teacherIsAdmin) {
        const languages = await helpers.getLanguages();

        this.languages = languages;
      }
    } catch (e) {
      console.log(e);
    }
  },
  methods: {
    async createFreeQuiz() {
      this.quizNameErrors = [];
      this.quizLanguageErrors = [];
      this.shortDescriptionErrors = [];
      this.createQuizError = false;

      if (!this.newQuizName) {
        this.quizNameErrors.push("Field Required");
      }

      if (!this.newQuizLanguage) {
        this.quizLanguageErrors.push("Field Required");
      }

      if (!this.newShortDescription) {
        this.shortDescriptionErrors.push("Field Required");
      }

      if (
        this.quizNameErrors.length ||
        this.quizLanguageErrors.length ||
        this.shortDescriptionErrors.length
      ) {
        return;
      }

      try {
        this.newQuizLoading = true;
        await helpers.createFreeQuiz(
          this.newQuizName,
          this.newQuizLanguage,
          this.newShortDescription
        );

        this.newQuizLoading = false;

        this.freeQuizzes.push({
          quiz_name: this.newQuizName,
          quiz_language: "Python",
          quiz_short_desc: this.newShortDescription
        });

        // Reset all form fields incase admin wants to create a second free quiz
        this.newQuizName = "";
        this.newQuizLanguage = null;
        this.newShortDescription = "";

        this.newQuizDialog = false;
      } catch (e) {
        this.newQuizLoading = false;
        this.createQuizError = true;
      }
    },
    generateUrl(qc_id) {
      return `/quizzes/instance/${qc_id}`;
    }
  }
};
</script>


<style lang="scss">
@import "../../styles/_mixins.scss";
@import "../../styles/_variables.scss";

#free-quizzes {
  background-color: #fff;
  @include card();
  padding: 0px 0px 0px 0px !important;

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

  #quiz-icon {
    font-size: 20px;
    color: $wet-asphalt;
    float: right !important;
  }

  #free-quizzes-pagination {
    display: flex;
    justify-content: center;
    bottom: 10px;
    margin-left: auto;
    margin-right: auto;
    left: 0;
    right: 0;
  }

  #new-free-quiz-btn {
    display: block;
    margin: 0 auto;
    margin-top: 10px;
    margin-bottom: 50px;
  }
}

#new-quiz-header {
  background-color: $wet-asphalt;
  color: #fff;
}
</style>



