<template>
    <v-card class="col-md-8 offset-md-2" id="courses">
        <h1>Courses</h1>
        <div class="row">
            <div class="col-sm-10">
                <v-text-field prepend-icon="title" label="Course Name" @input="$emit('update:courseName', cName)" :value="courseName" v-model="cName" color="secondary" maxlength="50" id="course-name"></v-text-field>
            </div>
            <div class="col-sm-2">
                <div id="create-box">
                    <v-btn id="create-btn" color="secondary" @click="addCourse(); cName = ''" depressed :disabled="courseName ? false : true">Create</v-btn>
                </div>
            </div>
        </div>
    </v-card>
</template>

<script>
import helpers from "./helpers";
export default {
  props: ["courseName", "addCourse"],
  data() {
    return {
      cName: null,
    };
  },
  async mounted() {},
  methods: {},
};
</script>

