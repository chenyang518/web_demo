<template>
  <div>
    <div class="row">
      <div class="col-12">
        <card>
          <template slot="header">
            <div class="row">
              <div class="col-sm-6" :class="isRTL ? 'text-right' : 'text-left'">
                <h1 class="card-title">{{$t('dashboard.laborReduction')}}</h1>
              </div>
              <div class="col-sm-6">
                <div class="btn-group btn-group-toggle"
                     :class="isRTL ? 'float-left' : 'float-right'"
                     data-toggle="buttons">
                  <label v-for="(option, index) in myChartCategories"
                         :key="option"
                         class="btn btn-sm btn-primary btn-simple"
                         :class="{active: myChart.activeIndex === index}"
                         :id="index">
                    <input type="radio"
                           @click="initChart(index)"
                           name="options" autocomplete="off"
                           :checked="myChart.activeIndex === index">
                    {{option}}
                  </label>
                </div>
              </div>
            </div>
          </template>
          <div class="chart-area">
            <my-chart id="chart" :chartData="myChart.chartData"/>
          </div>
        </card>
      </div>
    </div>

    <div class="row">
      <div class="col-12">
        <card :title="table.title">
          <div class="table-responsive">
            <base-table :data="table.data"
                        :columns="table.columns"
                        thead-classes="text-primary">
            </base-table>
          </div>
        </card>
      </div>
    </div>
  </div>
</template>

<script>
import * as chartConfigs from '@/components/Charts/config';
import config from '@/config';
import { BaseTable } from "@/components";
import MyChart from '../components/MyChart1';
import Card from '../components/Cards/Card.vue';
import axios from 'axios'

export default {
    components: {
      BaseTable,
      MyChart,
      Card,
    },
    data() {
      return {
        table: {
          columns: [],
          data: []
        },
        myChart: {
          activeIndex: 0,
          chartData: {
            months: [],
            data1: [],
            data2: []
          },
        },
        timer: {}
      }
    },
    computed: {
      enableRTL() {
        return this.$route.query.enableRTL;
      },
      isRTL() {
        return this.$rtl.isRTL;
      },
      myChartCategories() {
        return this.$t('dashboard.chart1Categories');
      },
    },
    methods: {
        initChart(index) {
            const path = 'http://localhost:5000/labor-reduction';
            axios.get(path)
                .then((res) => {
                    this.myChart.chartData.data1 = [];
                    this.myChart.chartData.data2 = [];
                    this.myChart.activeIndex = index;
                    index = (this.$t('dashboard.chart1Categories'))[index] + " Actual";
                    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                    for (var i in res.data) {
                        if (res.data[i]['Headcount'] == index) {
                            for (var j = 0; j < months.length; j++) {
                                this.myChart.chartData.data1.push(res.data[i][months[j]]);
                                this.myChart.chartData.data2.push(res.data[i-1][months[j]]);
                            }
                        }    
                    }
                    this.myChart.chartData.months = months;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        initTable() {
            const path = 'http://localhost:5000/labor-reduction';
            axios.get(path)
                .then((res) => {
                    this.table.columns = [];
                    this.table.data = [];
                    this.table.columns =['Headcount','Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                    var k = 1;
                    var data = [];
                    for (var i in res.data) {
                        if (i % 2 != 0) {
                        var temp = {
                            id: k++, headcount: res.data[i]['Headcount'],
                            jan: res.data[i]['Jan'], feb: res.data[i]['Feb'], mar: res.data[i]['Mar'], apr: res.data[i]['Apr'],
                            may: res.data[i]['May'], jun: res.data[i]['Jun'], jul: res.data[i]['Jul'], aug: res.data[i]['Aug'],
                            sep: res.data[i]['Sep'], oct: res.data[i]['Oct'], nov: res.data[i]['Nov'], dec: res.data[i]['Dec'], 
                        };
                        data.push(temp);
                        }
                    }
                    console.log(data);
                    this.table.data = [...data];
                    console.log(this.table.data);
                })
                .catch((error) => {
                    console.error(error);
                });
        }
    },
    mounted() {
      this.i18n = this.$i18n;
      if (this.enableRTL) {
        this.i18n.locale = 'ar';
        this.$rtl.enableRTL();
      }
      this.initChart(0);
      this.initTable();
    },
    created() {
        this.timer = setInterval(() => {
            this.initTable();
            this.initChart(this.myChart.activeIndex);
        }, 3000)
    },
    beforeDestroy() {
      if (this.$rtl.isRTL) {
        this.i18n.locale = 'en';
        this.$rtl.disableRTL();
      }
      clearInterval(this.timer);
    }
};
</script>

<style>

</style>