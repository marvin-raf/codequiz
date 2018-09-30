<template>
    <v-card class="col-md-8 offset-md-2" id="course">
        <h1>{{courseName}}: Quizzes</h1>

        <div class="row">
            <div class="col-sm-6">
                <v-text-field prepend-icon="title" label="Quiz Name" @input="$emit('update:quizName', $event)" :value="quizName" color="secondary" maxlength="50" id="quiz-name"></v-text-field>
            </div>
            <div class="col-sm-6">
                <v-select color="secondary" prepend-icon="language" :items="languages" @input="$emit('update:language', $event)" :value="language" item-text="language_name" item-value="language_id" label="Language" :nudge-left="200"></v-select>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-6">
                <v-menu color="secondary" ref="startDateMenu" :close-on-content-click="false" v-model="startDateMenu" :nudge-left="150" :nudge-top="200" :return-value.sync="startD" lazy transition="scale-transition" offset-y full-width min-width="290px">
                    <v-text-field color="secondary" slot="activator" v-model="startD" label="Start Date" prepend-icon="event" readonly></v-text-field>
                    <v-date-picker color="primary" v-model="startD" @input="$refs.startDateMenu.save(startD)"></v-date-picker>
                </v-menu>
            </div>
            <div class="col-sm-6">
                <v-menu color="secondary" ref="startTimeMenu" :close-on-content-click="false" v-model="startTimeMenu" :nudge-left="150" :nudge-top="200" :return-value.sync="startT" lazy transition="scale-transition" offset-y full-width max-width="290px" min-width="290px">
                    <v-text-field color="secondary" slot="activator" v-model="startT" label="Start Time" prepend-icon="access_time" readonly></v-text-field>
                    <v-time-picker color="primary" v-if="startTimeMenu" v-model="startT" @change="$refs.startTimeMenu.save(startT)"></v-time-picker>
                </v-menu>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-6">
                <v-menu color="secondary" ref="endDateMenu" :close-on-content-click="false" v-model="endDateMenu" :nudge-left="150" :nudge-top="200" :return-value.sync="endD" lazy transition="scale-transition" offset-y full-width min-width="290px">
                    <v-text-field color="secondary" slot="activator" v-model="endD" label="End Date" prepend-icon="event" readonly></v-text-field>
                    <v-date-picker color="primary" v-model="endD" @input="$refs.endDateMenu.save(endD)"></v-date-picker>
                </v-menu>
            </div>
            <div class="col-sm-6">
                <v-menu color="secondary" ref="endTimeMenu" :close-on-content-click="false" v-model="endTimeMenu" :nudge-left="150" :nudge-top="200" :return-value.sync="endT" lazy transition="scale-transition" offset-y full-width max-width="290px" min-width="290px">
                    <v-text-field color="secondary" slot="activator" v-model="endT" label="End Time" prepend-icon="access_time" readonly></v-text-field>
                    <v-time-picker color="primary" v-if="endTimeMenu" v-model="endT" @change="$refs.endTimeMenu.save(endT)"></v-time-picker>
                </v-menu>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-12">
                <v-textarea color="secondary" prepend-icon="info" name="description" label="Brief Description" @input="$emit('update:description', $event)" :value="description" maxlength="50"></v-textarea>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-12" style="text-align: center;">
                <v-btn v-if="!editMode && quizName && startD && startT && endD && endT && language" @click="createQuiz(startD, startT, endD, endT)" color="secondary" depressed>Create</v-btn>
                <v-btn v-if="!editMode && !quizName || !startD || !startT || !endD || !endT || !language" color="secondary" depressed disabled>Create</v-btn>
                <v-btn v-if="editMode && quizName && startD && startT && endD && endT && language" @click="editQuiz(startD, startT, endD, endT)" color="secondary" depressed>Save</v-btn>
                <v-btn v-if="editMode" @click="cancelEdit" color="error" depressed>Cancel</v-btn>
            </div>
        </div>
        <v-alert :value="showAlert" type="error">
            Dates order must be: Current Date
            < Start Date < End date </v-alert>

    </v-card>
</template>

<script>
import helpers from "./helpers";
export default {
  props: ["courseName", "courseId", "languages", "showAlert", "createQuiz", "editMode", "editQuiz", "cancelEdit", "quizName", "language", "startDate", "endDate", "startTime", "endTime", "description"],
  data() {
    return {
      //Quiz Info
      qName: "",
      lang: "",
      startD: "",
      startT: null,
      endD: "",
      endT: null,
      desc: "",

      //Date and Time picker menus
      startDateMenu: false,
      startTimeMenu: false,
      endDateMenu: false,
      endTimeMenu: false,
    };
  },
  async mounted() {},
  methods: {
    async create() {
      await this.createQuiz(this.startD, this.endD, this.startT, this.endT, this.courseId, this.qName, this.lang, this.desc);
      if (!this.showAlert) {
        this.qName = this.lang = this.startD = this.endD = this.desc = "";
        this.startT = this.endT = null;
      }
    },
    setEdit(startDate, startTime, endDate, endTime) {
      this.startD = startDate;
      this.startT = startTime;
      this.endD = endDate;
      this.endT = endTime;
    },
    reset() {
      this.startD = this.startT = this.endD = this.endT = null;
    },
  },
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