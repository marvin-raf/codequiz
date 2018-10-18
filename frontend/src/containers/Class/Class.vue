<template>
    <div>
        <v-card id="class-header" class="col-lg-10 offset-lg-1">
            <h1>Class goes here</h1>
        </v-card>

        <v-card class="col-lg-10 offset-lg-1" id="add-students">
            <h2>Add Students</h2>
            <div class="row">
                <div class="col-md-2">
                    <v-text-field label="Name" type="text" color="secondary"></v-text-field>
                </div>

                <div clas="col-md-5">
                    <v-text-field label="Name" type="text" color="secondary"></v-text-field>
                </div>

                <div class="col-md-2">
                    <v-btn flat color="secondary" style="margin-top: 15px;">Add</v-btn>
                </div>

            </div>

        </v-card>

        <v-card class="col-lg-10 offset-lg-1" id="students">
            <h2>Students</h2>
        </v-card>

    </div>

</template>

<script>
export default {
        
}
</script>

<style lang="scss">
@import "../../styles/_mixins.scss";

#class-header {
  @include dark-header();
}

#add-students {
  margin-top: 20px;
  text-align: center;
}

#students {
  margin-top: 20px;
  text-align: center;
}
</style>


