<template>
    <div>
        <v-card class="col-md-8 offset-md-2" id="course">
            <h1>{{courseName}}</h1>
        </v-card>
        <v-card class="col-md-8 offset-md-2" id="course">
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
        </v-card>
        <v-card class="col-md-8 offset-md-2" id="course">
            <v-list>
                <div v-for="(quiz, index) in quizzes.slice((page-1)*8, (page - 1) * 8 + 8)" v-bind:key="index">
                    <v-list-tile>
                        <v-list-title style="width: 100%;">
                            <div v-if="!quiz.input">
                                <a @click="$router.push('/quizzes/' + quiz.quiz_id)"> {{quiz.quiz_name}} </a>

                                <v-btn @click="changeInput(index, true)" color="secondary" depressed style="float: right;">Edit</v-btn>
                                <br> {{convert(quiz.quiz_start_date)}} - {{convert(quiz.quiz_end_date)}}
                            </div>
                            <div v-if="quiz.input">
                                <v-text-field color="secondary" maxlength="50" v-model="quizzes[index].quiz_name" style="float: left; width: 70%;"></v-text-field>
                                <v-btn @click="changeName(index, quiz.quiz_id, quiz.quiz_name)" color="secondary" depressed style="float: right;">Save</v-btn>
                            </div>
                        </v-list-title>
                        <v-list-content>
                        </v-list-content>

                    </v-list-tile>
                    <v-divider v-if="index != quizzes.length - 1"></v-divider>
                </div>
                <v-pagination color="secondary" :length="Math.ceil(quizzes.length / 8)" id="course-pagination" v-model="page"></v-pagination>
            </v-list>
        </v-card>
        <v-card class="col-md-8 offset-md-2" id="course">
            <h2>Classes</h2>
            <!--<v-select
            :items="teachClasses"
            label="Standard"
            ></v-select>-->
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
        </v-card>
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
      date: null
    };
  },
  async mounted() {
    try {
      this.course = await helpers.getCourse(this.$route.params.id);
      this.teachClasses = await helpers.getClasses();
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


