<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <a class="navbar-brand" href="#">covid.test</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <div class="navbar-nav mr-auto">
          <select class="form-control" @change="renderChartForCountry($event)">
            <option value="" selected disabled>Choose a country</option>
            <option v-for="country in countries" :key="country">{{ country }}</option>
          </select>
        </div>
        <div class="topnav-right">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item active">
              <a class="nav-link" data-toggle="modal" data-target="#creditsModal">Credits <span class="sr-only">(current)</span></a>
            </li>
          </ul>
          <div class="modal fade" id="creditsModal" tabindex="-1" role="dialog" aria-labelledby="creditsModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="creditsModalLabel">Credits</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <ul>
                    <li>Data made available by <a href="https://ourworldindata.org/coronavirus-testing">Our World in Data</a></li>
                    <br/>
                    <li></li>
                    <li>Presented by <a href="https://www.arjunrao.co">Arjun</a></li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <canvas id="covid-testing-chart"></canvas>
  </div>
</template>

<script>
const serverURL = process.env.SERVER_URL || "https://covid-testing-app.herokuapp.com"
export default {
  name: 'App',
  data() {
      return {
        countries: this.getCountries(),
      };
  },
  methods: {
    getCountries(){
      console.log("(ASYNC) Retrieving list of countries from server...")
      axios.get(serverURL + '/testing/countries').then(res => {
        this.countries = Object.keys(res['data'])
        console.log("Retrieved countries = ");
        console.log(this.countries);
      });
      axios.get(serverURL + '/testing/metrics').then(res => {
        console.log(res);
        this.metrics = res['data']['values']
      });
    },
    renderChartForCountry(event){
      var that = this
      console.log(event)
      axios.get(serverURL + '/testing/observations_for_country?country=' + event.target.value).then(res => {
        const ctx = document.getElementById('covid-testing-chart');
        const results = observations(res, that.metrics)
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
import observations from './observations.js';
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
ul {
  list-style-type: none;
}
</style>
