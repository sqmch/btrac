<template>
  <v-data-table
    :headers="headers"
    :items="issues"
    sort-by="calories"
    class="elevation-4"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>Tasks</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
              Add Task
            </v-btn>
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
              <v-btn color="blue darken-1" text @click="close"> Cancel </v-btn>
              <v-btn color="blue darken-1" text @click="save"> Save </v-btn>
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
              <v-btn color="blue darken-1" text @click="closeDelete"
                >Cancel</v-btn
              >
              <v-btn color="blue darken-1" text @click="deleteItemConfirm"
                >OK</v-btn
              >
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
    <template v-slot:no-data>
      <v-btn color="primary" @click="getIssues"> Reset </v-btn>
    </template>
  </v-data-table>
</template>
<script>
import axios from "axios";
export default {
  data: () => ({
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: "Title",
        align: "start",
        value: "title",
      },
      { text: "Details", value: "details" },
      { text: "Priority", value: "priority" },
      { text: "Status", value: "status" },
      { text: "Edit / Delete", value: "actions", sortable: false },
    ],
    statuses: ["Open", "In Progress", "Resolved"],
    priorities: ["Low", "Medium", "High"],
    issues: [],
    editedIndex: -1,
    editedItem: {
      title: "",
      details: "",
      priority: "",
      status: "",
    },
    defaultItem: {
      title: "",
      details: "",
      priority: "",
      status: "",
    },
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
      axios
        .get("http://127.0.0.1:1234/issues")
        .then((response) => {
          this.issues = response.data.Issues;
        })
        .catch((e) => {
          this.errors.push(e);
        });
    },
    addIssue() {
      axios.post("http://127.0.0.1:1234/issues", this.editedItem).then(
        (response) => {
          console.log(response);
        },
        (error) => {
          console.log(error);
        }
      );
    },
    putIssue() {
      axios
        .put(
          "http://127.0.0.1:1234/issues/" + this.editedItem.id,
          this.editedItem
        )
        .then(console.log(this.editedItem));
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
      axios.delete("http://127.0.0.1:1234/issues/" + this.editedItem.id);
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
