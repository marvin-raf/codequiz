import cookies from "js-cookie";

const teacherStore = {
    data : {
        teacherId : null,
        teacherName : null,
        teacherEmail : null,
        teacherIsAdmin : null
    },
    methods : {
        setData(json) {
            teacherStore.data.teacherId = json.teacher_id;
            teacherStore.data.teacherName = json.teacher_name;
            teacherStore.data.teacherEmail = json.teacher_email;
            teacherStore.data.teacherIsAdmin = json.teacher_is_admin;

        },
        teacherLoggedIn() {
            return teacherStore.data.teacherId !== null;
        },
        signout() {
            teacherStore.data.teacherId = null;
            teacherStore.data.teacherName = null;
            teacherStore.data.teacherEmail = null;
            teacherStore.data.teacherIsAdmin = null;
        }
    }
};

export default teacherStore;
