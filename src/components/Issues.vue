<template>
  <div>
    <!--
        <v-card><v-data-table
        item-key="title"
        :loading="issuesLoading"
        loading-text="Loading... Please wait"
        :headers="headers"
        :items="issues"
        sort-by="title"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Tracked items</v-toolbar-title>
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
                <v-btn
                  color="primary"
                  dark
                  class="mb-2"
                  v-bind="attrs"
                  v-on="on"
                >
                  Add item
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
              <v-card class="pa-4">
                <v-card-title class="headline">Delete</v-card-title>
                <v-card-text
                  >Are you sure you want to delete this item?</v-card-text
                >
                <v-card-actions>
                  <v-spacer></v-spacer>

                  <v-btn class="mx-4" color="primary " text @click="closeDelete"
                    >Cancel</v-btn
                  >
                  <v-btn
                    class="mx-4"
                    color="primary "
                    text
                    @click="deleteItemConfirm"
                    >Delete</v-btn
                  >
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon small class="mr-2" @click="editIssue(item)">
            mdi-pencil
          </v-icon>
          <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
        </template>
      </v-data-table>-->
    <v-card>
      <v-toolbar flat>
        <v-toolbar-title>Items</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-btn icon plain to="/projects">
          <v-icon>mdi-arrow-left</v-icon></v-btn
        >
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="500px">
          <template class="float-right" v-slot:activator="{ on, attrs }">
            <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
              Add item
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
              <v-btn color="primary " text @click="close"> Cancel </v-btn>
              <v-btn color="primary " text @click="save"> Save </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card class="pa-4">
            <v-card-title class="headline">Delete</v-card-title>
            <v-card-text
              >Are you sure you want to delete this item?</v-card-text
            >
            <v-card-actions>
              <v-spacer></v-spacer>

              <v-btn class="mx-4" color="primary " text @click="closeDelete"
                >Cancel</v-btn
              >
              <v-btn
                class="mx-4"
                color="primary "
                text
                @click="deleteItemConfirm"
                >Delete</v-btn
              >
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </v-card>
    <!-- main body -->
    <v-row>
      <v-col class="col-12">
        <v-container>
          <v-card>
            <v-toolbar flat>
              <v-toolbar-title> Open </v-toolbar-title>

              <v-btn class="mx-2" color="secondary" small fab text>
                {{ this.open_issues.length }}</v-btn
              >
              <v-divider class="mx-2" inset vertical></v-divider>

              <v-dialog v-model="dialog" max-width="500px">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn color="secondary" text fab v-bind="attrs" v-on="on">
                    <v-icon>mdi-plus</v-icon>
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
                    <v-btn color="primary " text @click="close"> Cancel </v-btn>
                    <v-btn color="primary " text @click="save"> Save </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
            <v-expansion-panels
              popout
              focusable
              class="mx-auto pa-6 my-2 ml-2"
              elevation="2"
            >
              <draggable
                group="issues"
                :list="open_issues"
                class="row list-group-item"
                @start="drag = true"
                @end="drag = false"
                @change="log"
              >
                <v-expansion-panel v-for="issue in open_issues" :key="issue.id">
                  <v-expansion-panel-header>
                    {{ issue.title }}
                  </v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <div class="py-4">{{ issue.details }}</div>

                    <v-btn
                      icon
                      class="my-2 mx-2 float-right"
                      @click="deleteItem(issue)"
                      ><v-icon> mdi-delete </v-icon></v-btn
                    >
                    <v-btn
                      icon
                      class="my-2 mx-2 float-right"
                      @click="editIssue(issue)"
                      ><v-icon> mdi-pencil </v-icon></v-btn
                    >
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </draggable>
            </v-expansion-panels>
          </v-card>
          <v-card
            ><v-toolbar flat>
              <v-toolbar-title> In Progress </v-toolbar-title>

              <v-btn class="mx-2" color="secondary" small fab text>
                {{ this.inprogress_issues.length }}</v-btn
              >
              <v-divider class="mx-2" inset vertical></v-divider>

              <v-dialog v-model="dialog" max-width="500px">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn color="secondary" text fab v-bind="attrs" v-on="on">
                    <v-icon>mdi-plus</v-icon>
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
                    <v-btn color="primary " text @click="close"> Cancel </v-btn>
                    <v-btn color="primary " text @click="save"> Save </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
            <v-expansion-panels
              popout
              focusable
              class="mx-auto pa-6 my-2 ml-2"
              elevation="2"
            >
              <draggable
                group="issues"
                :list="inprogress_issues"
                shaped
                class="row list-group-item"
                @start="drag = true"
                @end="drag = false"
                @change="listChange"
              >
                <v-expansion-panel
                  v-for="issue in inprogress_issues"
                  :key="issue.id"
                >
                  <v-expansion-panel-header>
                    {{ issue.title }}
                  </v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <div class="py-4">{{ issue.details }}</div>

                    <v-btn
                      icon
                      class="my-2 mx-2 float-right"
                      @click="deleteItem(issue)"
                      ><v-icon> mdi-delete </v-icon></v-btn
                    >
                    <v-btn
                      icon
                      class="my-2 mx-2 float-right"
                      @click="editIssue(issue)"
                      ><v-icon> mdi-pencil </v-icon></v-btn
                    >
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </draggable>
            </v-expansion-panels>
          </v-card>
          <v-card>
            <v-toolbar flat>
              <v-toolbar-title>
                <v-icon color="green">mdi-check</v-icon>
                Resolved
              </v-toolbar-title>

              <v-btn class="mx-2" color="green" small fab text>
                {{ this.resolved_issues.length }}</v-btn
              >
            </v-toolbar>
            <v-expansion-panels
              popout
              focusable
              class="mx-auto pa-6 my-2 ml-2"
              elevation="2"
            >
              <draggable
                group="issues"
                :list="resolved_issues"
                shaped
                class="row"
                @change="log"
              >
                <v-expansion-panel
                  v-for="issue in resolved_issues"
                  :key="issue.id"
                >
                  <v-expansion-panel-header>
                    {{ issue.title }}
                  </v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <div class="py-4">{{ issue.details }}</div>

                    <v-btn
                      icon
                      class="my-2 mx-2 float-right"
                      @click="deleteItem(issue)"
                      ><v-icon> mdi-delete </v-icon></v-btn
                    >
                    <v-btn
                      icon
                      class="my-2 mx-2 float-right"
                      @click="editIssue(issue)"
                      ><v-icon> mdi-pencil </v-icon></v-btn
                    >
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </draggable>
            </v-expansion-panels>
          </v-card>
        </v-container>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import axios from "axios";
import draggable from "vuedraggable";

export default {
  components: {
    draggable,
  },
  data: () => ({
    hover: false,
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
    open_issues: [],
    inprogress_issues: [],
    resolved_issues: [],
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
    dragOptions() {
      return {
        animation: 200,
        group: "description",
        disabled: false,
        ghostClass: "ghost",
      };
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
          this.open_issues = this.issues.filter((issue) =>
            issue.status.includes("Open")
          );
          this.inprogress_issues = this.issues.filter((issue) =>
            issue.status.includes("In Progress")
          );
          this.resolved_issues = this.issues.filter((issue) =>
            issue.status.includes("Resolved")
          );
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
            this.getIssues();
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
        this.getIssues();
      });
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
      this.getIssues();
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
        this.getIssues();
      } else {
        this.issues.push(this.editedItem);
        this.addIssue();
        this.getIssues();
      }
      this.close();
    },
    listChange() {
      //this.hover = true;
      console.log("lol");
      //console.log(this.hover);
    },
    add: function () {
      this.list.push({ name: "Juan" });
    },
    replace: function () {
      this.list = [{ name: "Edgard" }];
    },
    clone: function (el) {
      return {
        name: el.name + " cloned",
      };
    },
    log: function () {
      window.console.log("lol");
    },
  },
};
</script>
