<template>
    <div style="float: right">

        <v-snackbar v-model="notificationStore.showNotification" right :timeout="notificationStore.notificationTimeout">
            {{ notificationStore.notificationText }}
            <v-btn color="pink" flat @click="closeNotification()">
                Close
            </v-btn>
        </v-snackbar>
    </div>
</template>

<script>
import notificationStore from "../../store/notificationStore";

export default {
    data() {
        return {
            notificationStore: notificationStore.data,
        };
    },
    methods: {
        closeNotification() {
            notificationStore.methods.closeNotification();
        }
    }
}
</script>
