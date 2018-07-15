<template>
    <div id="dates" class="col-md-8 offset-md-2">
      <div v-if="this.editDateTime">
        <v-text-field label="Start Date" class="split-fields" color="secondary" type="date" v-model="editStartDate" :error-messages="editStartDateErrors"></v-text-field>
        <v-text-field label="Start Time" class="split-fields" color="secondary" type="time" v-model="editStartTime" :error-messages="editStartTimeErrors"></v-text-field>

        <!--Used so that the v-card expands-->
        <div style="clear: both;"></div>

        <v-text-field label="End Date" class="split-fields" color="secondary" type="date" v-model="editEndDate" :error-messages="editEndDateErrors"></v-text-field>
        <v-text-field label="End Time" class="split-fields" color="secondary" type="time" v-model="editEndTime" :error-messages="editEndTimeErrors"></v-text-field>

        <!--Used so that the v-card expands-->
        <div style="clear: both;"></div>

        </div>

        <div v-else id="date-time-frame">
          {{ parseDate() }}
        </div>


        <div id="edit-btns">
          <v-btn id="edit-cancel-time" @click="cancel()" v-if="editDateTime" >Cancel</v-btn>
          <div style="clear: both;"></div>
        </div>

        
        
    </div>
</template>

<script>
import helpers from "./helpers";

export default {
  props: ["startDate", "startTime", "endDate", "endTime", "editDateTime"],
  data() {
    return {
      editStartDate: this.startDate,
      editStartTime: this.startTime,
      editEndDate: this.endDate,
      editEndTime: this.endTime,
      editStartDateErrors: [],
      editStartTimeErrors: [],
      editEndDateErrors: [],
      editEndTimeErrors: []
    };
  },
  methods: {
    editSave() {
      if (this.editDateTime) {
        // Reset errors
        this.editStartDateErrors = [];
        this.editStartTimeErrors = [];
        this.editEndDateErrors = [];
        this.editEndTimeErrors = [];

        // Check for errors
        if (!this.editStartDate) {
          this.editStartDateErrors.push("Field Required");
        }

        if (!this.editStartTime) {
          this.editStartTimeErrors.push("Field Required");
        }

        if (!this.editEndDateErrors) {
          this.editEndDateErrors.push("Field Required");
        }

        if (!this.editEndTimeErrors) {
          this.editEndTimeErrors.push("Field Required");
        }

        const errorFound =
          this.editStartDateErrors.length ||
          this.editStartTimeErrors.length ||
          this.editEndDateErrors.length ||
          this.editEndTimeErrors.length;

        if (errorFound) return;

        this.$emit("save-date-time", {
          startDate: this.editStartDate,
          startTime: this.editStartTime,
          endDate: this.editEndDate,
          endTime: this.editEndTime
        });
      } else {
        this.$emit("toggle-edit-date-time");
      }
    },
    parseDate() {
      return helpers.parseDate(
        this.startDate,
        this.startTime,
        this.endDate,
        this.endTime
      );
    },
    cancel() {
      // Resetting the editing values to the initial values
      this.editStartDate = this.startDate;
      this.editStarTime = this.startTime;
      this.editEndDate = this.endDate;
      this.editEndTime = this.endTime;

      this.$emit("toggle-edit-date-time");
    }
  },
  mounted() {}
};
</script>

<style lang="scss">
@import "../../../styles/_variables.scss";
#edit-save-time {
  background-color: $emerald;
  color: #fff;
  display: block;
}

#date-time-frame {
  text-align: center;
}

#edit-cancel-time {
  background-color: $emerald;
  color: #fff;
}

#edit-btns {
  width: 300px;
  margin: 0 auto;
}
</style>
