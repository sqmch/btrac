<template>
  <v-data-table
    item-key="title"
    :loading="issuesLoading"
    loading-text="Loading... Please wait"
    :headers="headers"
    :items="issues"
    sort-by="title"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>Tasks</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>

        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
              Add Issue
            </v-btn>
            <v-btn dark class="mb-2 mr-5" to="/projects">
              Back to projects</v-btn
            >
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-text-field
                  v-model="editedItem.title"
                  label="Title"
                ></v-text-field>

                <v-textarea
                  name="Details"
                  v-model="editedItem.details"
                  label="Details"
                ></v-textarea>
                <v-select
                  v-model="editedItem.priority"
                  label="Priority"
                  :items="priorities"
                  outlined
                ></v-select>
                <v-select
                  :items="statuses"
                  v-model="editedItem.status"
                  label="Status"
                  outlined
                ></v-select>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary " text @click="close"> Cancel </v-btn>
              <v-btn color="primary " text @click="save"> Save </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="headline"
              >Are you sure you want to delete this item?</v-card-title
            >
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary " text @click="closeDelete">Cancel</v-btn>
              <v-btn color="primary " text @click="deleteItemConfirm">OK</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:[`item.actions`]="{ item }">
      <v-icon small class="mr-2" @click="editIssue(item)"> mdi-pencil </v-icon>
      <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
    </template>
  </v-data-table>
</template>
<script>
import axios from "axios";
export default {
  data: () => ({
    search: "",
    issuesLoading: false,
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: "Title",
        align: "start",
        value: "title",
      },
      //{ text: "Details", value: "details" },
      { text: "Status", value: "status" },
      { text: "Priority", value: "priority" },
      { text: "Edit / Delete", value: "actions", sortable: false },
    ],
    statuses: ["Open", "In Progress", "Resolved"],
    priorities: ["Low", "Medium", "High"],
    issues: [],
    editedIndex: -1,
    editedItem: {
      title: "",
      details: "",
      status: "",
      priority: "",
    },
    defaultItem: {
      title: "",
      details: "",
      status: "",
      priority: "",
    },
    selectedProjectId: null,
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "Add Task" : "Edit Task";
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  created() {
    this.getIssues();
  },

  methods: {
    getIssues() {
      this.issuesLoading = true;
      axios
        .get(`/projects/${this.$store.state.project_id}/issues`, {
          headers: { Authorization: "Bearer " + this.$store.state.token },
        })
        .then((response) => {
          this.issues = response.data.Issues;
          this.issuesLoading = false;
        })
        .catch((e) => {
          console.log(e);
        });
    },
    addIssue() {
      axios
        .post(
          `/projects/${this.$store.state.project_id}/issues`,
          this.editedItem,
          {
            headers: { Authorization: "Bearer " + this.$store.state.token },
          }
        )
        .then(
          (response) => {
            console.log(response);
          },
          (error) => {
            console.log(error);
          }
        );
    },
    putIssue() {
      axios({
        method: "put",
        url: `/issues/${this.editedItem.id}`,
        headers: { Authorization: "Bearer " + this.$store.state.token },
        data: this.editedItem,
      }).catch((e) => {
        console.log(e);
      });
      /*axios
        .put(`/issues/${this.editedItem.id}`, this.editedItem, {
          headers: { Authorization: "Bearer " + this.$store.state.token },
        })
        .then(console.log(this.editedItem)).catch((e) => {
        console.log(e);
      });

        */
    },

    editIssue(item) {
      this.editedIndex = this.issues.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedIndex = this.issues.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.issues.splice(this.editedIndex, 1);
      axios
        .delete(`http://127.0.0.1:1234/issues/${this.editedItem.id}`, {
          headers: { Authorization: "Bearer " + this.$store.state.token },
        })
        .catch((e) => {
          console.log(e);
        });
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.issues[this.editedIndex], this.editedItem);
        this.putIssue();
      } else {
        this.issues.push(this.editedItem);
        this.addIssue();
      }
      this.close();
    },
  },
};
</script>
