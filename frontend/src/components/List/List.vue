<template>
    <v-list>
        <!--.slice call gets only the quizzes we want on the specific page of the pagination-->
        <div v-for="(item, index) in getItems()" v-bind:key="index">
            <v-divider v-if="index === 0"></v-divider>
            <ListItem :item="item" :idKey="idKey" :nameKey="nameKey" :descriptionKey="descriptionKey" :generateUrl="generateUrl" :icon="icon" />
            <v-divider></v-divider>
        </div>
    </v-list>
</template>

<script>
          
import ListItem from "./ListItem/ListItem";


export default {
    components: {
        ListItem
    },
    /*
    The props key, descriptionKey and generateUrl are used to allow
    flexibility so this list component can be used for quizzes, courses, classes etc. 
    */
    props: ["items", "page", "perPage", "idKey", "nameKey", "descriptionKey", "generateUrl", "icon"],
    data() {
        return {

        };
    },
    methods: {
        // Gets index of page to slice from
        getItems() {
            return this.items.slice((this.page - 1) * this.perPage, ((this.page - 1) * this.perPage) + this.perPage);
        }
    }
}</script>

