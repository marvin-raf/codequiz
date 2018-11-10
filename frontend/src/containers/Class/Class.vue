<template>
    <div>
        <DeleteModal :deleteModal="deleteStudentModal.modal" :confirmEvent="deleteStudent" :cancelEvent="() => {deleteStudentModal.modal = false;}" />

        <v-card id="class-header" class="col-lg-10 offset-lg-1">
            <v-progress-circular indeterminate color="secondary" class="class-loader" v-if="className === null"></v-progress-circular>

            <h1 v-else>{{ className }}</h1>

        </v-card>

        <v-card class="col-lg-10 offset-lg-1" id="add-students">

            <h2>Add Students</h2>
            <div class="row">
                <v-text-field label="Name" type="text" color="secondary" class="col-md-6" :error-messages="nameErrors" v-model="studentName" :maxlength="50"></v-text-field>

                <v-text-field label="Email" type="text" color="secondary" class="col-md-6" :error-messages="emailErrors" v-model="studentEmail" :maxlength="128"></v-text-field>
            </div>

            <v-btn flat id="add-class-btn" @click="addStudent">Add</v-btn>
            <br>
            <span>OR</span>

            <br>

            <v-btn id="upload-spreadsheet">Upload</v-btn>

        </v-card>

        <v-card class="col-lg-10 offset-lg-1" id="students" style="padding-bottom: 10px;">
            <h2>Students</h2>

            <div v-if="students === null">
                <v-progress-circular indeterminate color="secondary" class="class-loader" v-if="className === null" style="margin-top: 100px;"></v-progress-circular>
            </div>

            <div v-else>
                <v-data-table :headers="headers" :items="students" no-data-text="No Students" class="elevation-1" hide-actions>
                    <template slot="items" slot-scope="props">
                        <td class="text-xs-left">
                            {{ props.item.student_id }}
                        </td>
                        <td class="text-xs-left">
                            {{ props.item.student_name }}
                        </td>
                        <td class="text-xs-left">
                            {{ props.item.student_email }}
                        </td>

                        <td class="text-xs-left">
                            <v-icon>{{ props.item.student_activated ? "done" : "close" }}</v-icon>
                        </td>

                        <td class="text-xs-right">
                            <v-icon color="primary" class="delete-icon" @click="openModal(props.item.student_id, props.index)">
                                delete
                            </v-icon>
                        </td>
                    </template>
                </v-data-table>

            </div>

        </v-card>

    </div>

</template>

<script>
import DeleteModal from "../../components/DeleteModal/DeleteModal";
import notificationStore from "../../store/notificationStore";

import helpers from "./helpers";

import validator from "email-validator";


export default {
    components: {
        DeleteModal,
    },
    data() {
        return {
        helloworld: false,
        studentName: "",
        studentEmail: "",
        classId: null,
        className: null,
        students: null,
        nameErrors: [],
        emailErrors: [],
        // All data to do with deleting a student
        deleteStudentModal: {
            modal: false,
            studentId: null,
            studentIndex: null
        },
        headers: [
        {
          text: "Student ID",
          sortable: false,
          value: "student_id"
        },
        {
          text: "Student Name",
          sortable: false,
          value: "student_name"
        },
        {
          text: "Student Email",
          sortable: false,
          value: "student_email"
        },
        {
            text: "Activated",
            sortable: false,
            value: "activated"
        },
        {
          text: "Actions",
          sortable: false,
          value: "actions",
          align: "right"
        }
      ]
        };
    },
    async mounted() {
        const { classId, className } = await helpers.getClass(this.$route.params.id);
        this.classId = classId;
        this.className = className;

        const students = await helpers.getStudents(this.$route.params.id);


        console.log(students);

        this.students = students;

        
    },
    methods: {
        /*
        Resets, checks and sets errors. Returns true if an error was found,
        returns false otherwise
        */
        addStudentError() {
            return new Promise(async (resolve, reject) => {
            this.nameErrors = [];
            this.emailErrors = [];

            // Check for new errors
            if (!this.studentName) {
                this.nameErrors.push("Field Required");
            }

            if (!this.studentEmail) {
                this.emailErrors.push("Field Required");
            } else if (!validator.validate(this.studentEmail)) {
                this.emailErrors.push("Invalid Email");
            } else {
                const emailUsed = await helpers.checkEmailExists(this.$route.params.id, this.studentEmail)

                if (emailUsed) {
                    this.emailErrors.push("Email already taken");
                }
            }

            

            if (this.nameErrors.length || this.emailErrors.length) {
                resolve(true);
                return;
            }

                resolve(false);
            })
        },
        // Adds a single student to a class
        async addStudent() {
            try {
                if (!(await this.addStudentError())) {
                    console.log("I made it here");
                    const students = await helpers.addStudents(this.$route.params.id, [{name: this.studentName, email: this.studentEmail}]);              

                    this.students = students;

                    this.studentName = "";
                    this.studentEmail = "";
                } 
            } catch (e) {
                // PLEASE CHANGE THIS LATER TO DIALOGS
                console.log(e);
            }
            
         
            
            
        },
        async deleteStudent() {
            try {
                await helpers.deleteStudent(this.$route.params.id, this.deleteStudentModal.studentId);
                notificationStore.methods.showNotification({
                    text: "Student Deleted",
                    isError: false,
                });

                
                this.students.splice(this.deleteStudentModal.studentIndex, 1);

            } catch (e) {
                notificationStore.methods.showNotification({
                    text: "Error Deleting Student",
                    isError: true,
                });

            }

            this.deleteStudentModal = {
                modal: false,
                studentId: null,
                studentIndex: null
            }
        },
        openModal(studentId, studentIndex) {
            this.deleteStudentModal = {
                modal: true,
                studentId,
                studentIndex
            }
        }
    }
}
</script>

<style lang="scss">
@import "../../styles/_mixins.scss";
@import "../../styles/_variables.scss";

#class-header {
  @include dark-header();
}

#add-students {
  padding-top: 20px;
  margin-top: 20px;
  text-align: center;
}

#students {
  padding-top: 20px;
  margin-top: 20px;
  text-align: center;
  min-height: 300px;
}

#add-class-btn {
  @include emerald-btn();
}

#upload-spreadsheet {
  @include emerald-btn();
}

.class-loader {
  display: block;
  margin: 0 auto;
}

.edit-icon {
  cursor: pointer;

  &:hover {
    color: $emerald !important;
  }
}

.delete-icon {
  cursor: pointer;

  &:hover {
    color: $ALIZARIN !important;
  }
}
</style>


