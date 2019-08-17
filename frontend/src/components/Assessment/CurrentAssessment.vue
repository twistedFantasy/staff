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
          <div slot="header" class="checkpoint">
            <div>{{checkpoint.title}}</div>
            <div class="checkpoint-data">{{checkpoint.date}}</div>
          </div>
          <v-card>
            <v-card-text>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</v-card-text>
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
    checkpoints: state => state.assessment.allCheckpoints
  }),
  created() {
    this.getCheckpoints(this.$route);
  },
  methods: {
    ...mapActions({
      getCheckpoints: "assessment/getCheckpoints"
    })
  }
};
</script>

<style>
.assessment {
  display: flex;
  flex-direction: row;
  width: 100%;
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
</style>

