<template>
    <div>
        <v-card class="col-lg-10 offset-lg-1" id="class-header">
            <h1>Classes</h1>
        </v-card>

        <v-card id="class-content" class="col-lg-10 offset-lg-1">
            <div id="class-loader" v-if="classes === null">
                <v-progress-circular color="secondary" indeterminate>
                </v-progress-circular>
            </div>

            <div v-else>
                <List :items="classes" :page="page" :perPage="8" idKey="class_id" nameKey="class_name" :generateUrl="generateUrl"></List>

                <v-pagination color="secondary" :length="Math.ceil(classes.length / PER_PAGE)" id="classes-pagination" v-model="page"></v-pagination>
            </div>

        </v-card>

    </div>
</template>

<script>
import helpers from "./helpers";

import List from "../../components/List/List";


export default {
    components: {
        List
    },
    data() {
        return {
            classes: null,
            page: 1,
            PER_PAGE: 8
        };
    },
    async mounted() {
        try {
            const classes = await helpers.getClasses();

            this.classes = classes;

        } catch (e) {
            console.log(e);
        }
    },
    methods: {
        generateUrl(class_id) {
            return `/classes/${class_id}`;
        }
    }
}
</script>



<style lang="scss">
@import "../../styles/_mixins.scss";

#class-header {
  @include dark-header();
}

#class-content {
  margin-top: 10px;
  min-height: 300px;
  padding-top: 20px;
}

#class-loader {
  margin: 0 auto;
  display: block;
  width: 50px;
  text-align: center;
  margin-top: 50px;
}

#classes-pagination {
  display: flex;
  justify-content: center;
  bottom: 10px;
  margin-left: auto;
  margin-right: auto;
  left: 0;
  right: 0;
}
</style>

