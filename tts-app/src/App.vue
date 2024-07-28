<template>
  <div id="app">
    <TTS />
  </div>
</template>

<script>
import TTS from './components/TTS.vue'

export default {
  name: 'App',
  components: {
    TTS
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 100px;
}

body {
  margin: 0;
  background: url('../public/color4bg.png') no-repeat center center fixed;
  background-size: cover;
}
</style>
