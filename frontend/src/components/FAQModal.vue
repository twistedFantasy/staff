<template>
  <div v-bind:class="{ 'modal-container open': visible, 'modal-container close': !visible }">
    <div class="faq-title">FAQ
      <div class="close-icon" @click="onClose"> <v-icon>close</v-icon></div>
    </div>
    <div class="faq-content">
       <div v-for="faq in faqs" v-bind:key="faq.name">
         <div v-if="faq.active">
         <div class="question">{{faq.question}} :</div>
          <div class="answer">{{faq.answer}}</div>
          </div>
       </div>
    </div>
    
  </div>
  
</template>

<script>
import * as absenceService from "../services/absence.service";
export default {
  
  props: {
    onClose: { type: Function },
    visible: { type: Boolean }
  },
    data: () => ({
    faqs: [],
    
  }),
  created() {
    this.getFAQ();
  },
   methods: {
    //make action
    getFAQ() {
      absenceService
        .getFAQContent()
        .then(data => {
          this.$store.dispatch("absence/setFAQ", data.results);
          this.faqs = data.results;
        })
        .catch(error => {
          console.log(error, "error");
        });
    }
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
  font-size: 20px!important;
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
