<template>
  <div v-bind:class="{ 'modal-container open': visible, 'modal-container close': !visible }">
    <div class="faq-title">
      FAQ
      <div class="close-icon" @click="onClose">
        <v-icon>close</v-icon>
      </div>
    </div>
    <div class="faq-content">
      <div v-for="item in faq" v-bind:key="item.name">
        <div v-if="item.active">
          <div class="question">{{item.question}} :</div>
          <div class="answer">{{item.answer}}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
export default {
  props: {
    onClose: { type: Function },
    visible: { type: Boolean }
  },
  data: () => ({}),
  computed: mapState({
    faq: state => state.user.faq
  }),
  created() {
    this.getFAQ();
  },
  methods: {
    ...mapActions({
      getFAQ: "user/getFAQ" // проксирует `this.getUserProfile()` в `this.$store.dispatch('user/getUser')`
    })
  }
};
</script>

<style>
.modal-container {
  position: fixed;
  top: 0;
  margin: auto;
  width: 30%;
  height: 100%;
  transform: translate3d(0%, 0, 0);
  z-index: 100;
  overflow-y: auto;
  background-color: white;
  border-radius: 2px;
}

.open {
  right: 0;
  transition: opacity 0.3s linear, right 0.3s ease-out;
}

.close {
  right: -30%;
  transition: opacity 0.3s linear, right 0.3s ease-out;
}
.faq-title {
  position: relative;
  padding: 20px;
  font-size: 20px !important;
  margin-bottom: 10px;
  border-bottom: 1px solid;
}

.close-icon {
  position: absolute;
  top: 5px;
  right: 5px;
  cursor: pointer;
}
.faq-content {
  padding: 20px;
}
.question {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
}
.answer {
  margin-bottom: 10px;
  font-size: 12px;
}
</style>
