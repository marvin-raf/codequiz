<template>
    <div>
        <v-card class="col-md-8 offset-md-2" id="course">
            <h1>{{courseName}}: Quizzes</h1>
            <div class="row">
                <div class="col-sm-6">
                    <v-text-field prepend-icon="title" label="Quiz Name" v-model="quizName" color="secondary" maxlength="50" id="quiz-name"></v-text-field>
                </div>
                <div class="col-sm-6">
                    <v-select color="secondary" prepend-icon="language" :items="languages" v-model="language" item-text="language_name" item-value="language_id" label="Language" :nudge-left="200"></v-select>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-6">
                    <v-menu color="secondary" ref="menu" :close-on-content-click="false" v-model="menu" :nudge-left="150" :nudge-top="200" :return-value.sync="start_date" lazy transition="scale-transition" offset-y full-width min-width="290px">
                        <v-text-field color="secondary" slot="activator" v-model="start_date" label="Start Date" prepend-icon="event" readonly></v-text-field>
                        <v-date-picker color="primary" v-model="start_date" @input="$refs.menu.save(start_date)"></v-date-picker>
                    </v-menu>
                </div>
                <div class="col-sm-6">
                    <v-menu color="secondary" ref="menu2" :close-on-content-click="false" v-model="menu2" :nudge-left="150" :nudge-top="200" :return-value.sync="start_time" lazy transition="scale-transition" offset-y full-width max-width="290px" min-width="290px">
                        <v-text-field color="secondary" slot="activator" v-model="start_time" label="Start Time" prepend-icon="access_time" readonly></v-text-field>
                        <v-time-picker color="primary" v-if="menu2" v-model="start_time" @change="$refs.menu2.save(start_time)"></v-time-picker>
                    </v-menu>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-6">
                    <v-menu color="secondary" ref="menu3" :close-on-content-click="false" v-model="menu3" :nudge-left="150" :nudge-top="200" :return-value.sync="end_date" lazy transition="scale-transition" offset-y full-width min-width="290px">
                        <v-text-field color="secondary" slot="activator" v-model="end_date" label="End Date" prepend-icon="event" readonly></v-text-field>
                        <v-date-picker color="primary" v-model="end_date" @input="$refs.menu3.save(end_date)"></v-date-picker>
                    </v-menu>
                </div>
                <div class="col-sm-6">
                    <v-menu color="secondary" ref="menu4" :close-on-content-click="false" v-model="menu4" :nudge-left="150" :nudge-top="200" :return-value.sync="end_time" lazy transition="scale-transition" offset-y full-width max-width="290px" min-width="290px">
                        <v-text-field color="secondary" slot="activator" v-model="end_time" label="End Time" prepend-icon="access_time" readonly></v-text-field>
                        <v-time-picker color="primary" v-if="menu4" v-model="end_time" @change="$refs.menu4.save(end_time)"></v-time-picker>
                    </v-menu>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-12">
                    <v-textarea color="secondary" prepend-icon="info" name="description" label="Brief Description" value="" v-model="description" maxlength="50"></v-textarea>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-12" style="text-align: center;">
                    <v-btn v-if="quizName && start_date && start_time && end_date && end_time && language" @click="createQuiz" color="secondary" depressed>Create</v-btn>
                    <v-btn v-if="!quizName || !start_date || !start_time || !end_date || !end_time || !language" color="secondary" depressed disabled>Create</v-btn>
                </div>
            </div>
            <v-alert :value="showAlert" type="error">
                Dates order must be: Current Date
                < Start Date < End date </v-alert>

        </v-card>
        <!--<v-card class="col-md-8 offset-md-2" id="course">
            <h2>Quizzes</h2>
            <div class="row">
                <div class="col-sm-5">
                    <v-text-field label="Quiz Name" v-model="quizName" color="secondary" maxlength="50" id="quiz-name"></v-text-field>
                </div>
                <div class="col-sm-5">
                    <v-menu ref="menu" :close-on-content-click="false" v-model="menu" :nudge-left="100" :return-value.sync="date" lazy transition="scale-transition" offset-y full-width min-width="290px">
                        <v-text-field slot="activator" v-model="date" label="Picker in menu" prepend-icon="event" readonly></v-text-field>
                        <v-date-picker v-model="date" no-title scrollable>
                            <v-spacer></v-spacer>
                            <v-btn flat color="primary" @click="menu = false">Cancel</v-btn>
                            <v-btn flat color="primary" @click="$refs.menu.save(date)">OK</v-btn>
                        </v-date-picker>
                    </v-menu>

                </div>
            </div>
        </v-card>-->
        <v-card class="col-md-8 offset-md-2" id="course">
            <v-list>
                <div v-for="(quiz, index) in quizzes.slice((page-1)*8, (page - 1) * 8 + 8)" v-bind:key="index">
                    <v-list-tile style="height: 50px;">
                        <v-list-tile-title style="width: 100%; height: 45px;">
                            <div v-if="!quiz.input">
                                <a @click="$router.push('/quizzes/' + quiz.quiz_id)"> {{quiz.quiz_name}} </a>

                                <v-btn @click="setupEdit(index)" flat style="min-width: 50px; width: 50px; float: right;">
                                    <v-icon>edit</v-icon>
                                </v-btn>
                                <br>
                                <div style="font-size: 14px; color: grey;">{{convert(quiz.quiz_start_date)}} - {{convert(quiz.quiz_end_date)}}</div>
                            </div>
                            <div v-if="quiz.input">
                                <v-text-field color="secondary" maxlength="50" v-model="quizzes[index].quiz_name" style="float: left; width: 70%;"></v-text-field>
                                <v-btn @click="changeName(index, quiz.quiz_id, quiz.quiz_name)" color="secondary" depressed style="min-width: 50px; width: 50px; float: right;">Save</v-btn>
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
        <!--<v-card class="col-md-8 offset-md-2" id="course">
            <h2>Classes</h2>
            <v-select
            :items="teachClasses"
            label="Standard"
            ></v-select>
            <div id="create-box">
                <v-btn id="create-btn" color="secondary" @click="addClass()" depressed :disabled="className ? false : true" style="float: right; margin-right: 24px;">Add</v-btn>
            </div>
        </v-card>
        <v-card class="col-md-8 offset-md-2" id="course">
            <v-list>
                <div v-for="(clas, index) in classes.slice((page2-1)*8, (page2 - 1) * 8 + 8)" v-bind:key="index">
                    <v-list-tile>
                        <v-list-title style="width: 100%;">
                            <div v-if="!clas.input">
                                {{clas.class_name}}
                                <v-btn @click="changeInputC(index, true)" color="secondary" depressed style="float: right;">Edit</v-btn>
                            </div>
                            <div v-if="clas.input">
                                <v-text-field color="secondary" maxlength="50" v-model="classes[index].class_name" style="float: left; width: 70%;"></v-text-field>
                                <v-btn @click="changeClass(index, clas.class_id, clas.class_name)" color="secondary" depressed style="float: right;">Save</v-btn>
                            </div>
                        </v-list-title>
                        <v-list-content>
                        </v-list-content>

                    </v-list-tile>
                    <v-divider v-if="index != classes.length - 1"></v-divider>
                </div>
                <v-pagination color="secondary" :length="Math.ceil(classes.length / 8)" id="course-pagination" v-model="page2"></v-pagination>
            </v-list>
        </v-card>-->
    </div>
</template>

<script>
import helpers from "./helpers";

import teacherStore from "../../store/teacherStore.js";
import studentStore from "../../store/studentStore.js";
export default {
  data() {
    return {
      course: null,
      courseName: null,
      courseId: this.$route.params.id,
      quizzes: [],
      classes: [],
      quizName: null,
      page: 1,
      page2: 1,
      className: null,
      teachClasses: [],
      menu: null,
      menu2: null,
      menu3: null,
      menu4: null,
      start_date: null,
      start_time: null,
      end_date: null,
      end_time: null,
      languages: [],
      language: null,
      description: "",
      showAlert: false
    };
  },
  async mounted() {
    try {
      this.course = await helpers.getCourse(this.$route.params.id);
      this.teachClasses = await helpers.getClasses();
      this.languages = await helpers.getLanguages();
      console.log(this.languages);
      console.log(this.teachClasses);
      this.courseName = this.course.course.course_name;
      this.quizzes = this.course.course.course_quizzes;
      this.classes = this.course.course.course_classes;
      for (let i = 0; i < this.quizzes.length; i++) {
        //this.quizzes[i].input = false;
      }
      for (let i = 0; i < this.classes.length; i++) {
        //this.classes[i].input = false;
      }
    } catch (e) {
      console.log(e);
      this.$router.push("/dashboard");
    }
  },
  methods: {
    async addClass() {
      try {
        const { classId } = await helpers.addClass(
          this.className,
          this.courseId
        );
        this.classes.push({
          class_name: this.quizName,
          class_id: classId
        });
        this.className = null;
      } catch (e) {
        console.log(e);
      }
    },
    convert: function(date) {
      date = date * 1000;
      return (
        helpers.getDateTime(date).date + " " + helpers.getDateTime(date).time
      );
    },
    convertBack: function(date) {
        return "yeet lmao"
    },
    setupEdit: function(i) {
        this.quizName = this.quizzes[i].quiz_name;
        this.description = this.quizzes[i].quiz_short_desc;
        this.language = this.quizzes[i].quiz_language_id;
        this.start_date = this.quizzes[i].quiz_start_date;
        
    },
    async changeName(index, id, name) {
      try {
        await helpers.changeName(id, name);
      } catch (e) {
        console.log(e);
      }
      this.$set(this.quizzes[index], "input", false);
    },
    async changeClass(index, id, name) {
      try {
        await helpers.changeClass(id, name);
      } catch (e) {
        console.log(e);
      }
      this.$set(this.classes[index], "input", false);
    },
    async createQuiz() {
        this.showAlert = false;
        console.log(this.language);
        let start_date = new Date(this.start_date).getTime() / 1000 - 43200;
        let end_date = new Date(this.end_date).getTime() / 1000 - 43200;

        let start_time = this.start_time.split(':');
        start_time = parseInt(start_time[0]) * 60 * 60 + parseInt(start_time[1]) * 60; 

        let end_time = this.end_time.split(':');
        end_time = parseInt(end_time[0]) * 60 * 60 + parseInt(end_time[1]) * 60;        
        try {
            let quizId = await helpers.createQuiz(this.courseId, this.quizName, start_date+start_time, end_date+end_time, this.language, this.description);
            this.quizzes.push({
                quiz_name: this.quizName,
                quiz_id: quizId.quiz_id,
                quiz_start_date: start_date+start_time,
                quiz_end_date: end_date+end_time,
                quiz_language_id: this.language,
                quiz_short_desc: this.description

            });
        } catch (e) {
            console.log(e);
            this.showAlert = true;
        }
        
    },
    changeInput: function(index, value) {
      this.$set(this.quizzes[index], "input", value);
    },
    changeInputC: function(index, value) {
      this.$set(this.classes[index], "input", value);
    }
  }
};
</script>

<style lang="scss">
@import "../../styles/_mixins.scss";
@import "../../styles/_variables.scss";
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


