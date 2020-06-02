<template>
  <div id="app">
    <canvas id="planet-chart"></canvas>
  </div>
</template>

<script>

export default {
  name: 'App',
  data() {
    return {
      chartData: chartData,
    }
  },
  mounted() {
    this.createChart('planet-chart', this.chartData);
  },
  methods: {
    createChart(chartId, chartData) {
      const ctx = document.getElementById(chartId);
      new Chart(ctx, {
        type: chartData.type,
        data: chartData.data,
        options: chartData.options,
      });
    }
  }
}
import Chart from 'chart.js'
import chartData from './chart-data.js';
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
