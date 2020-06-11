<template>
  <div id="app">
    <select class="form-control" @change="renderChartForCountry($event)">
      <option value="" selected disabled>Choose</option>
      <option v-for="country in countries" :key="country">{{ country }}</option>
    </select>
    <canvas id="covid-testing-chart"></canvas>
  </div>
</template>

<script>

export default {
  name: 'App',
  data() {
      return {
        countries: this.getCountries()
      };
  },
  mounted() {
    this.createChart('covid-testing-chart');
  },
  methods: {
    getCountries(){
      console.log( "***********")
      axios.get('http://127.0.0.1:5000/testing/countries').then(res => {
        console.log( ">>>>>>>>>>>>")
        console.log(res['data'])
        this.countries = res['data'].split(',')
      })
    },
    renderChartForCountry(event){
      const country = event.target.value.replace(/'/g,'');
      console.log("Coun" + country)

      axios.get('http://127.0.0.1:5000/testing/observations_for_country?country='+country).then(res => {
        console.log(res)
        const chartId = 'covid-testing-chart'
        const ctx = document.getElementById(chartId);
        const results = observations(res)
        new Chart(ctx, {
          type: results.type,
          data: results.data,
          options: results.options,
        });
      })
    },
    createChart(chartId) {
      axios.get('http://127.0.0.1:5000/testing/observations_for_country?country=India').then(res => {
        console.log(res)
        const ctx = document.getElementById(chartId);
        const results = observations(res)
        new Chart(ctx, {
          type: results.type,
          data: results.data,
          options: results.options,
        });
      })
    }
  }
}
import Chart from 'chart.js'
import observations from './data/observations.js';
import axios from 'axios';
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  margin: 0 auto;
}
/* .canvas{
  position: relative; 
  height:80vh; 
  width:85vw
} */
</style>
