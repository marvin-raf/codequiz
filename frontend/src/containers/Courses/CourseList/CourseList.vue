<template>
    <v-card class="col-md-8 offset-md-2" id="courses">
        <v-list>
            <div v-for="(course, index) in courses.slice(pageIndex(), pageIndex() + 8)" v-bind:key="index">
                <v-list-tile id="course-tile">
                    <v-list-tile-title id="course-tile-title">
                        <div v-if="!course.input">
                            <a @click="$router.push('/courses/' + course.course_id)"> {{course.course_name}} </a>
                            <v-btn id="course-edit-btn" @click="changeInput(index + pageIndex(), true)" flat>
                                <v-icon>edit</v-icon>
                            </v-btn>
                        </div>
                        <div v-if="course.input">
                            <div class="row">
                                <div class="col-sm-10">
                                    <v-text-field id="course-edit-field" color="secondary" maxlength="50" v-model="courses[index + pageIndex()].course_name"></v-text-field>
                                </div>
                                <div class="col-sm-2">
                                    <v-btn id="course-save-btn" @click="changeName(index + pageIndex(), course.course_id, course.course_name)" color="secondary" depressed>Save</v-btn>
                                </div>
                            </div>
                        </div>
                    </v-list-tile-title>
                    <v-list-tile-content>
                    </v-list-tile-content>
                </v-list-tile>
                <v-divider v-if="index != courses.length - 1"></v-divider>
            </div>
            <v-pagination color="secondary" :length="Math.ceil(courses.length / 8)" id="courses-pagination" v-model="page"></v-pagination>
        </v-list>
    </v-card>
</template>

<script>
import helpers from "./helpers";
export default {
  props: ["courses", "changeName", "changeInput"],
  data() {
    return {
      page: 1,
    };
  },
  async mounted() {},
  methods: {
    pageIndex: function() {
      return (this.page - 1) * 8;
    },
  },
};
</script>

<style lang="scss">
@import "../../../styles/_mixins.scss";
@import "../../../styles/_variables.scss";
#courses {
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

#courses-pagination {
  display: flex;
  justify-content: center;
}

#course-tile {
  height: 50px;
}

#course-tile-title {
  width: 100%;
  height: 45px;
}

#course-edit-btn {
  min-width: 50px;
  width: 50px;
  float: right;
}

#course-edit-field {
  float: left;
}

#course-save-btn {
  min-width: 50px;
  width: 50px;
  float: right;
}
</style>