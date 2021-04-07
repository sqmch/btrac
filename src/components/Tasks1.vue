<template>
  <v-data-table
    :headers="headers"
    :items="issues"
    sort-by="title"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>Tasks</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
      </v-toolbar>
    </template>
  </v-data-table>
</template>
<script>
import axios from "axios";
export default {
  data: () => ({
    headers: [
      {
        text: "Title",
        align: "start",
        value: "title",
      },
      { text: "Priority", value: "priority" },
      { text: "Status", value: "status" },
    ],
    issues: [],
  }),

  computed: {},

  mounted() {
    this.getIssues();
  },
  created() {
    this.getIssues();
  },

  methods: {
    getIssues() {
      axios
        .get("http://127.0.0.1:1234/issues")
        .then((response) => {
          this.issues = response.data.Issues;
        })
        .catch((e) => {
          this.errors.push(e);
        });
    },
  },
};
</script>
