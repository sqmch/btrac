<template>
  <div>
    <v-card flat>
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
            <v-btn large color="primary" dark class="" v-bind="attrs" v-on="on">
              <v-icon class="mr-2">mdi-plus</v-icon>Add task
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
        <v-dialog
          :retain-focus="false"
          v-model="dialogDelete"
          max-width="500px"
        >
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
      <v-col class="pa-2 col-12">
        <v-container flat>
          <v-card flat class="">
            <v-toolbar class="" flat>
              <v-toolbar-title>
                <v-icon class="mr-3">mdi-format-list-checks</v-icon> Task
              </v-toolbar-title>

              <v-btn class="ml-2" color="secondary" small fab text>
                {{ this.openIssues.length }}</v-btn
              >

              <v-divider class="ml-3" inset vertical></v-divider>

              <v-dialog
                :retain-focus="false"
                v-model="dialog"
                max-width="500px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    color="secondary"
                    class="ml-4"
                    small
                    text
                    fab
                    v-bind="attrs"
                    v-on="on"
                  >
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
            <v-expansion-panels flat focusable class="my-2 pa-0">
              <draggable
                :empty-insert-threshold="200"
                group="issues"
                :list="openIssues"
                shaped
                class="col-12 list-group"
                v-bind="dragOptions"
                @change="onEnd"
                @start="drag = true"
                @end="drag = false"
              >
                <transition-group
                  type="transition"
                  :name="!drag ? 'flip-list' : null"
                >
                  <div v-for="issue in openIssues" :key="issue.id">
                    <v-expansion-panel>
                      <v-expansion-panel-header>
                        {{ issue.title }}
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <div
                          :class="
                            issue.fixed
                              ? 'fa fa-anchor'
                              : 'glyphicon glyphicon-pushpin'
                          "
                          @click="issue.fixed = !issue.fixed"
                          aria-hidden="true"
                        >
                          <p class="my-4">
                            {{ issue.details }}
                          </p>
                        </div>

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
                        <v-btn
                          icon
                          class="my-2 mx-2 float-right"
                          @click="finishIssue(issue)"
                          ><v-icon> mdi-check </v-icon></v-btn
                        >
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                  </div>
                </transition-group>
              </draggable>
            </v-expansion-panels>
          </v-card>

          <v-card>
            <v-toolbar flat>
              <v-toolbar-title>
                <v-icon class="mr-3" color="green">mdi-check</v-icon>
                Done
              </v-toolbar-title>

              <v-btn class="mx-2" color="green" small fab text>
                {{ this.resolvedIssues.length }}</v-btn
              >
            </v-toolbar>
            <v-expansion-panels popout focusable class="my-2" elevation="2">
              <draggable
                :empty-insert-threshold="200"
                group="issues"
                :list="resolvedIssues"
                shaped
                class="col-12 my-2 list-group"
                v-bind="dragOptions"
                @change="onEnd"
                @start="drag = true"
                @end="drag = false"
                ><transition-group
                  type="transition"
                  :name="!drag ? 'flip-list' : null"
                >
                  <div v-for="issue in resolvedIssues" :key="issue.id">
                    <v-expansion-panel>
                      <v-expansion-panel-header>
                        {{ issue.title }}
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <div
                          :class="
                            issue.fixed
                              ? 'fa fa-anchor'
                              : 'glyphicon glyphicon-pushpin'
                          "
                          @click="issue.fixed = !issue.fixed"
                          aria-hidden="true"
                        >
                          <p class="my-4">
                            {{ issue.details }}
                          </p>
                        </div>

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
                  </div>
                </transition-group>
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
const message = [
  "vue.draggable",
  "draggable",
  "component",
  "for",
  "vue.js 2.0",
  "based",
  "on",
  "Sortablejs",
];
export default {
  components: {
    draggable,
  },
  data: () => ({
    drag: false,
    list: message.map((name, index) => {
      return { name, id: index + 1 };
    }),
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
      { text: "Edit / Delete", value: "actions", sortable: false },
    ],
    statuses: ["Open", "Resolved"],
    issues: [],
    openIssues: [],
    resolvedIssues: [],
    orderedOpenIssues: [],
    orderedResolvedIssues: [],
    editedIndex: -1,
    editedItem: {
      title: "",
      details: "",
      status: "",
    },
    defaultItem: {
      title: "",
      details: "",
      status: "",
    },
    selectedProjectId: 1,
    issueOrder: {},
    rawIssueOrder: null,

    openIssueOrderStr: "",
    openIssueOrderArr: [],

    resolvedIssueOrderStr: "",
    resolvedIssueOrderArr: [],
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

  mounted() {
    this.getIssues();
    this.getProjectIssueOrder();
  },

  methods: {
    getIssues() {
      this.issuesLoading = true;
      if (this.$store.state.project_id) {
        axios
          .get(`/projects/${this.$store.state.project_id}/issues`, {
            headers: { Authorization: "Bearer " + this.$store.state.token },
          })
          .then((response) => {
            this.issues = response.data.Issues;
            this.openIssues = this.issues.filter((issue) =>
              issue.status.includes("Open")
            );
            this.resolvedIssues = this.issues.filter((issue) =>
              issue.status.includes("Resolved")
            );
            this.issuesLoading = false;
          })
          .catch((e) => {
            console.log(e);
          });
      }
    },
    separateIssues() {},
    addIssue() {
      if (this.$store.state.project_id) {
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
      }
    },
    putIssue() {
      axios({
        method: "put",
        url: `/issues/${this.editedItem.id}`,
        headers: { Authorization: "Bearer " + this.$store.state.token },
        data: this.editedItem,
      })
        .then()
        .catch((e) => {
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

    finishIssue(issue) {
      this.editedItem.title = issue.title;
      this.editedItem.details = issue.details;
      this.editedItem.id = issue.id;
      this.editedItem.status = "Resolved";
      this.putIssue();
      this.editedItem.title = "";
      this.editedItem.details = "";
      this.editedItem.id = "";
      this.getIssues();
    },
    onEnd(evt) {
      if (evt.moved) {
        this.updateProjectIssueOrder();
        this.getProjectIssueOrder();
      }
      if (evt.added) {
        this.editedItem.title = evt.added.element.title;
        this.editedItem.details = evt.added.element.details;
        this.editedItem.id = evt.added.element.id;
        if (evt.added.element.status === "Open") {
          this.editedItem.status = "Resolved";
        } else {
          this.editedItem.status = "Open";
        }
        this.updateProjectIssueOrder();
        this.getProjectIssueOrder();

        this.putIssue();
        this.editedItem.title = "";
        this.editedItem.details = "";
        this.editedItem.id = "";
      }
    },
    createIssueOrderArrays() {
      this.resolvedIssueOrderArr = [];
      for (let index = 0; index < this.resolvedIssues.length; index++) {
        try {
          this.resolvedIssueOrderArr.push(this.resolvedIssues[index]);
        } catch (e) {
          console.log(e);
        }
      }
      this.openIssueOrderArr = [];
      for (let index = 0; index < this.openIssues.length; index++) {
        try {
          this.openIssueOrderArr.push(this.openIssues[index]);
        } catch (e) {
          console.log(e);
        }
      }
    },
    currentIssueOrder() {
      this.createIssueOrderArrays();
      return {
        open_issues: this.openIssueOrderArr,
        resolved_issues: this.resolvedIssueOrderArr,
      };
    },
    updateProjectIssueOrder() {
      let current_order = this.currentIssueOrder();
      axios({
        method: "put",
        url: `/projects/${this.$store.state.project_id}/order`,
        headers: { Authorization: "Bearer " + this.$store.state.token },
        data: { order: current_order },
      })
        .then()
        .catch((e) => {
          console.log(e);
        });
    },
    getProjectIssueOrder() {
      axios({
        method: "get",
        url: `/projects/${this.$store.state.project_id}/getorder`,
        headers: { Authorization: "Bearer " + this.$store.state.token },
      })
        .then((response) => {
          let clean_response = JSON.parse(
            response.data["order"].replaceAll("'", '"')
          )["order"];
          this.issueOrder = clean_response;
          this.openIssues = this.issueOrder.open_issues;
          this.resolvedIssues = this.issueOrder.resolved_issues;
          this.createIssueOrderArrays();
        })
        .catch((e) => {
          console.log(e);
        });
    },
  },
};
</script>
<style>
.flip-list-move {
  transition: transform 0.5s;
}
.no-move {
  transition: transform 0s;
}
.ghost {
  opacity: 0.5;
  background: #c8ebfb;
}
.list-group {
  min-height: 50px;
}
.list-group-item {
  cursor: move;
}
.list-group-item i {
  cursor: pointer;
}
.v-expansion-panel::before {
  box-shadow: 1px;
}
</style>
