import cookies from "js-cookie";

const teacherStore = {
  data: {
    teacherId: null,
    teacherName: null,
    teacherEmail: null
  },
  methods: {
    setData(json) {
      teacherStore.data.teacherId = json.teacher_id;
      teacherStore.data.teacherName = json.teacher_name;
      teacherStore.data.teacherEmail = json.teacher_email;
    },
    teacherLoggedIn() {
      return teacherStore.data.teacherId !== null;
    },
    logout() {
      teacherStore.data.teacherId = null;
      teacherStore.data.teacherName = null;
      teacherStore.data.teacherEmail = null;
    }
  }
};

export default teacherStore;
