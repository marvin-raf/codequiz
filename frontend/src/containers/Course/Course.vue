<template>
    <div>
        {{editIndex}}
        <AddQuiz :courseName="courseName" :courseId="courseId" :languages="languages" :showAlert="showAlert" :createQuiz="createQuiz" :editMode="editMode" :quizName.sync="quizName" :language.sync="language" :startDate.sync="startDate" :endDate.sync="endDate" :startTime.sync="startTime" :endTime.sync="endTime" :description.sync="description" :editQuiz="editQuiz" :cancelEdit="cancelEdit" ref="AddQuiz"></AddQuiz>
        <QuizList :quizzes="quizzes" :setupEdit="setupEdit" :convert="convert"></QuizList>
    </div>
</template>

<script>
import helpers from "./helpers";

//Auth
import teacherStore from "../../store/teacherStore.js";
import studentStore from "../../store/studentStore.js";

//Components
import AddQuiz from "./AddQuiz/AddQuiz.vue";
import QuizList from "./QuizList/QuizList.vue";

export default {
  components: {
    AddQuiz,
    QuizList,
  },
  data() {
    return {
      //course info
      course: null,
      courseName: null,
      courseId: this.$route.params.id,
      quizzes: [],

      //create quiz info
      quizName: "",
      startDate: null,
      startTime: null,
      endDate: null,
      endTime: null,
      languages: [],
      language: null,
      description: "",

      //for editing quizzes
      editMode: false,
      editIndex: null,

      showAlert: false,
    };
  },
  async mounted() {
    this.getCourse();
  },
  methods: {
    convert: function(date) {
      date = date * 1000;
      return helpers.getDateTime(date).date + " " + helpers.getDateTime(date).time;
    },
    async getCourse() {
      try {
        this.course = await helpers.getCourse(this.$route.params.id);
        this.languages = await helpers.getLanguages();
        this.courseName = this.course.course.course_name;
        this.quizzes = this.course.course.course_quizzes;
      } catch (e) {
        console.log(e);
        this.$router.push("/dashboard");
      }
    },
    setupEdit(i) {
      if (this.editIndex != null) {
        this.quizzes[this.editIndex].input = false;
      }
      this.quizName = this.quizzes[i].quiz_name;
      this.description = this.quizzes[i].quiz_short_desc;
      this.language = this.quizzes[i].quiz_language_id;
      [this.startDate, this.startTime] = helpers.convertDate(this.quizzes[i].quiz_start_date);
      [this.endDate, this.endTime] = helpers.convertDate(this.quizzes[i].quiz_end_date);
      this.editMode = true;
      this.quizzes[i].input = true;
      this.editIndex = i;
      this.$refs.AddQuiz.setEdit(this.startDate, this.startTime, this.endDate, this.endTime);
    },
    cancelEdit() {
      this.resetFields();
      this.editMode = false;
      this.quizzes[this.editIndex].input = false;
      this.editIndex = null;
    },
    getDates(startDate, startTime, endDate, endTime) {
      startDate = new Date(startDate).getTime() / 1000 - 43200;
      endDate = new Date(endDate).getTime() / 1000 - 43200;

      startTime = startTime.split(":");
      startTime = parseInt(startTime[0]) * 60 * 60 + parseInt(startTime[1]) * 60;
      endTime = endTime.split(":");
      endTime = parseInt(endTime[0]) * 60 * 60 + parseInt(endTime[1]) * 60;
      return [startDate, startTime, endDate, endTime];
    },
    async createQuiz(startDate, startTime, endDate, endTime) {
      this.showAlert = false;
      [startDate, startTime, endDate, endTime] = this.getDates(startDate, startTime, endDate, endTime);

      try {
        let quizId = await helpers.createQuiz(this.courseId, this.quizName, startDate + startTime, endDate + endTime, this.language, this.description);
        this.quizzes.push({
          quiz_name: this.quizName,
          quiz_id: quizId.quiz_id,
          quiz_start_date: startDate + startTime,
          quiz_end_date: endDate + endTime,
          quiz_language_id: this.language,
          quiz_short_desc: this.description,
        });
        this.resetFields();
      } catch (e) {
        console.log(e);
        this.showAlert = true;
      }
    },
    resetFields() {
      this.quizName = this.language = this.description = "";
      this.$refs.AddQuiz.reset();
    },
    async editQuiz(startDate, startTime, endDate, endTime) {
      this.showAlert = false;
      [startDate, startTime, endDate, endTime] = this.getDates(startDate, startTime, endDate, endTime);
      try {
        helpers.editQuiz(this.quizzes[this.editIndex].quiz_id, this.quizName, startDate + startTime, endDate + endTime, this.language, this.description);
        this.$set(this.quizzes, this.editIndex, {
          quiz_name: this.quizName,
          quiz_id: this.quizzes[this.editIndex].quiz_id,
          quiz_start_date: startDate + startTime,
          quiz_end_date: endDate + endTime,
          quiz_language_id: this.language,
          quiz_short_desc: this.description,
        });
        console.log(this.quizzes[this.editIndex]);
        this.resetFields();
        this.editIndex = null;
        this.editMode = false;
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
    },
  },
};
</script>



