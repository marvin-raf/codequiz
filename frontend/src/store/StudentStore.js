const studentStore = {
  data: {
    studentId: null,
    studentName: null,
    teacherId: null,
    teacherName: null,
    studentEmail: null
  },
  methods: {
    setData(teacherStore) {
      studentStore.data.studentId = teacherStore.student_id;
      studentStore.data.studentName = teacherStore.student_name;
      studentStore.data.teacherId = teacherStore.teacher_id;
      studentStore.data.teacherName = teacherStore.teacher_name;
      studentStore.data.studentEmail = teacherStore.student_email;
    },
    teacherLoggedIn() {
      return studentStore.data.teacherId !== null;
    },
    logout() {
      studentStore.data.studentId = null;
      studentStore.data.studentName = null;
      studentStore.data.teacherId = null;
      studentStore.data.teacherName = null;
      studentStore.data.studentEmail = null;
    }
  }
};

export default studentStore;
