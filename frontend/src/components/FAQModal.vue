<template>
  <div v-bind:class="{ 'modal-container open': visible, 'modal-container close': !visible }">
    <div>Vjlfk</div>
    <div @click="onClose">Close</div>
  </div>
  
</template>

<script>
export default {
  props: {
    onClose: { type: Function },
    visible: { type: Boolean }
  }
};
</script>

<style>
.modal-container {
  position: fixed;
  top: 0;
  margin: auto;
  width: 320px;
  height: 100%;
  transform: translate3d(0%, 0, 0);
  z-index: 100;
  overflow-y: auto;
  background-color: white;
  padding: 15px;
  border-radius: 2px;
}

.open {
  right: 0;
  transition: opacity 0.3s linear, right 0.3s ease-out;
}

.close {
  right: -320px;
  transition: opacity 0.3s linear, right 0.3s ease-out;
}
</style>
