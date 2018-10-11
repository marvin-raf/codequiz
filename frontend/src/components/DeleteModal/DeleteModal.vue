<template>
    <div>

        <v-dialog persistent :value="deleteModal" width="500">

            <v-card>
                <v-card-title class="headline red lighten-1 justify-center" primary-title>
                    <span style="color: #fff;">Are you sure?</span>
                </v-card-title>

                <v-divider></v-divider>
                <v-card-actions style="width: 200px;margin: 0 auto;">
                    <v-btn color="primary" flat @click="cancelEvent()">
                        Go Back
                    </v-btn>

                    <v-btn color="red lighten-1" flat @click="confirmEvent()">
                        Delete
                    </v-btn>

                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
export default {
    props: ["deleteModal", "confirmEvent", "cancelEvent"]
}
</script>

