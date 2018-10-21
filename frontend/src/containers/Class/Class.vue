<template>
    <div>
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

        <v-card class="col-lg-10 offset-lg-1" id="students">
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

                        <td class="text-xs-right">
                            <v-icon color="primary">
                                edit
                            </v-icon>
                            <v-icon color="primary">
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
import helpers from "./helpers";

import validator from "email-validator";


export default {
    data() {
        return {
        studentName: "",
        studentEmail: "",
        classId: null,
        className: null,
        students: null,
        nameErrors: [],
        emailErrors: [],
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

        this.students = students;

        
    },
    methods: {
        /*
        Resets, checks and sets errors. Returns true if an error was found,
        returns false otherwise
        */
        async addStudentError() {
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
                const emailNotUsed = await helpers.checkEmailExists(this.$route.params.id, this.studentEmail)

                if (!emailNotUsed) {
                    this.emailErrors.push("Email already taken");
                }
            }

            



            if (this.nameErrors.length || this.emailErrors.length) {
                return true;
            }

            return false;
        },
        // Adds a single student to a class
        async addStudent() {
            try {
                if (!this.addStudentError()) {
                    console.log("I made it here");
                    await helpers.addStudents(this.$route.params.id, [{name: this.studentName, email: this.studentEmail}]);              
                    this.studentName = "";
                    this.studentEmail = "";
                } else {
                    console.log("Oops, I made it here");
                }
            } catch (e) {
                // PLEASE CHANGE THIS LATER TO DIALOGS
                console.log(e);
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
</style>


