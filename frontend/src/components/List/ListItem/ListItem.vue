<template>
    <v-list-tile @click="$router.push(generateUrl(item[idKey]))">

        <span>
            <div class="name-key">
                <a @click="$router.push(generateUrl(item[idKey]))" href="#">{{ item[nameKey] }}</a>

            </div>

        </span>

        <v-list-tile-content style="width: 100%;margin-left:20px">
            <div class="short-description" v-if="item[descriptionKey]">

                {{ item[descriptionKey] }}

            </div>

        </v-list-tile-content>
        <font-awesome-icon v-if="icon" :icon="icon" id="quiz-icon" />

    </v-list-tile>
</template>

<script>
export default {
    props: ["item", "idKey", "nameKey","descriptionKey", "generateUrl", "icon"]
}
</script>

<style lang="scss">
a {
  text-decoration: none;
}

.name-key {
  width: 100px;
  float: left;
}

.short-description {
  float: left;
}
</style>


