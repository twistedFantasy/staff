<template>
  <div class="assessment">
    <div class="desc-block">
      <div class="item-tab">
        <div class="title">Assessment period:</div>
        <div class="desc">Mar17-Mar19</div>
      </div>
      <div class="item-tab">
        <div class="title">Plan</div>
        <div class="desc">Mar17-Mar19</div>
      </div>
      <div class="item-tab">
        <div class="title">Description</div>
        <div class="desc">
          drgreger gregergb trhtrhrts srnsnthynj ynsnsgtnj yntysngbsr jfotunb;
          srthbkyhjthklt
          tkhjmrthpjmw'tpoj orjhptohpot hptjhpijthpirjth yptojhpotjh ptoyhjpto4h
          jto rphjprtoj ptjhpotijhtp eorkgjo tipogyjto tphojmptohj p9thojpo4thj
          r4thop4o5tkjhp o9j4po5hjyo4pt kj4hp9kpo4j9 4ophtj6hporheoiridtj ortjuho
          wseti5yjhhoi 4oi5yjo45i o4ijy45oirjyoitj5yig5jtigjroy oiht4ohyji56yj
        </div>
      </div>
    </div>
    <div class="table-block">
      <v-expansion-panel>
        <v-expansion-panel-content v-for="(checkpoint,i) in checkpoints" :key="i">
          <div @click="onChange(e,checkpoint)" slot="header" class="checkpoint">
            <div>{{checkpoint.title}}</div>
            <div class="checkpoint-data">{{checkpoint.date}}</div>
          </div>
          <v-card>
            <v-card-text>
              <div v-for="(task,i) in tasks" :key="i" class="task-container">
                <div class="title-task">{{task.title}}</div>
                <div class="desc-task">{{task.description}}</div>
                <v-icon v-if="task.completed" small class="icon mr-2">check_circle</v-icon>
                <v-icon v-if="!task.completed" small class="icon mr-2">mdi-watch</v-icon>
              </div>
            </v-card-text>
          </v-card>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  computed: mapState({
    checkpoints: state => state.assessment.allCheckpoints,
    tasks: state => state.assessment.tasksOfCheckpoint
  }),
  created() {
    this.getCheckpoints(this.$route);
  },
  methods: {
    ...mapActions({
      getCheckpoints: "assessment/getCheckpoints",
      getTasksByCheckpoints: "assessment/getTasksByCheckpoints"
    }),
    onChange(a, b) {
      console.log(a, "a");
      this.getTasksByCheckpoints(b.id);
    }
  }
};
</script>

<style>
.assessment {
  display: flex;
  flex-direction: row;
  width: 100%;
}
.assessment .v-icon.material-icons.theme--light {
  background: unset !important;
}
.desc-block {
  width: 50%;
}
.table-block {
  width: 50%;
}
.assessment .title {
  font-size: 20px;
  margin-bottom: 5px;
}
.item-tab {
  margin-bottom: 15px;
}
.desc {
  margin-left: 10px;
  max-width: 600px;
  color: rgba(102, 164, 212, 0.5);
}
.table-row {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  margin: 10px;
  height: 40px;
  font-size: 16px;
  border: 1px solid rgba(102, 164, 212, 0.5);
  width: 400px;
}
.v-expansion-panel__header {
  background: #003851;
  color: #66a4d4;
}
.theme--light.v-expansion-panel .v-expansion-panel__container {
  background: #003851;
}
.checkpoint {
  display: flex;
  justify-content: space-between;
}
.v-expansion-panel {
  width: 600px;
}
.checkpoint-data {
  margin-right: 22px;
}
.v-card__text {
  background: #12466edb;
  color: #66a4d4;
}
.task-container {
  padding: 10px;
  border-bottom: 1px solid #66a4d4;
  display: flex;
  justify-content: space-between;
}
.title-task {
  width: 18%;
  font-weight: bold;
  color: #004478;
  font-size: 15px;
}
.desc-task {
  max-width: 400px;
  overflow-y: scroll;
  overflow-x: hidden;
  max-height: 150px;
  width: 70%;
}
.desc-task::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  border-radius: 12px;
  background-color: #004478;
}

.desc-task::-webkit-scrollbar {
  width: 6px;
  background-color: #004478;
}
.desc-task::-webkit-scrollbar-thumb {
  border-radius: 12px;
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  background-color: #66a4d4;
}
</style>

