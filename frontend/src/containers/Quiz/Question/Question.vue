<template>
    <v-card class="question col-md-8 offset-md-2">
        <h3>Question 1</h3>


        <vue-markdown>
            {{ question.question_description }}

        </vue-markdown>

        <v-divider></v-divider>

  <v-data-table
    :headers="headers"
    :items="testCases"
    hide-actions
    class="elevation-1"
  >
    <template slot="items" slot-scope="props">
      <td v-bind:class="{ 'question-right': props.item.expected === props.item.actual, 'question-wrong': props.item.expected !== props.item.actual }"> <pre>{{ props.item.testCase }}</pre></td>
      <td v-bind:class="{ 'question-right': props.item.expected === props.item.actual,  'question-wrong': props.item.expected !== props.item.actual}"><pre>{{ props.item.expected }}</pre></td>
      <td v-bind:class="{ 'question-right': props.item.expected === props.item.actual, 'question-wrong': props.item.expected !== props.item.actual}"><pre>{{ props.item.actual }}</pre></td>
    </template>
  </v-data-table>



    </v-card>
</template>

<script>
import VueMarkdown from "vue-markdown";

export default {
  props: ["question"],
  components: {
    "vue-markdown": VueMarkdown
  },
  data() {
    return {
      headers: [
        {
          text: "Test Case",
          sortable: false,
          value: "testCase"
        },
        {
          text: "Expected",
          sortable: false,
          value: "expected"
        },
        {
          text: "Actual",
          sortable: false,
          value: "actual"
        }
      ],
      testCases: [
        {
          testCase: "print(sum(3, 4))",
          expected: "7",
          actual: "7"
        },
        {
          testCase: "print(sum(3, 9))",
          expected: "12",
          actual: "13"
        }
      ]
    };
  }
};
</script>


<style lang="scss">
@import "../../../styles/_variables.scss";
.question {
  margin-top: 30px;
  padding: 10px;
}

.question-right {
  background-color: rgba(46, 204, 113, 0.5);
}

.question-wrong {
  background-color: rgba(231, 76, 60, 0.5);
}
</style>

