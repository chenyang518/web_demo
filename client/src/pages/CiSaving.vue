<template>
  <div>
    <div class="row">
      <div class="col-12">
        <card>
          <template slot="header">
            <div class="row">
              <div class="col-sm-6" :class="isRTL ? 'text-right' : 'text-left'">
                <h1 class="card-title">{{$t('dashboard.ciSaving')}}</h1>
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
import MyChart from '../components/MyChart2';
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
        return this.$t('dashboard.chart2Categories');
      },
    },
    methods: {
        initChart() {
            const path = 'http://localhost:5000/ci-saving';
            axios.get(path)
                .then((res) => {
                    this.myChart.chartData.data1 = [];
                    this.myChart.chartData.data2 = [];
                    var data_New = [];
                    var data_Carryover = [];
                    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                    for (var i in res.data) {
                        if (res.data[i]['CI Saving(WRMB)'] == "Keiper Accumulative Total-New") {
                            for (var j = 0; j < months.length; j++) {
                                data_New.push(res.data[i][months[j]]);
                            }
                        }
                        else if (res.data[i]['CI Saving(WRMB)'] == "Keiper Accumulative Total-Carryover") {
                            for (var j = 0; j < months.length; j++) {
                                data_Carryover.push(res.data[i][months[j]]);
                            }
                        }
                        else if (res.data[i]['CI Saving(WRMB)'] == "Target") {
                            for (var j = 0; j < months.length; j++) {
                                this.myChart.chartData.data2.push(res.data[i][months[j]]);
                            }
                        }
                    }
                    console.log(data_New);
                    for (var j = 0; j < months.length; j++) {
                        this.myChart.chartData.data1.push(data_New[j]+data_Carryover[j]);
                    }
                    this.myChart.chartData.months = months;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        initTable() {
            const path = 'http://localhost:5000/ci-saving';
            axios.get(path)
                .then((res) => {
                    this.table.columns = [];
                    this.table.data = [];
                    this.table.columns =['CiSaving','YTDTarget', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                    var k = 1;
                    var data = [];
                    for (var i in res.data) {
                        var temp = {
                            id: k++, cisaving: res.data[i]['CI Saving(WRMB)'], ytdtarget: res.data[i]['YTD Target'],
                            jan: res.data[i]['Jan'], feb: res.data[i]['Feb'], mar: res.data[i]['Mar'], apr: res.data[i]['Apr'],
                            may: res.data[i]['May'], jun: res.data[i]['Jun'], jul: res.data[i]['Jul'], aug: res.data[i]['Aug'],
                            sep: res.data[i]['Sep'], oct: res.data[i]['Oct'], nov: res.data[i]['Nov'], dec: res.data[i]['Dec'], 
                        };
                        data.push(temp);
                    }
                    this.table.data = [...data];
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
      this.initChart();
      this.initTable();
    },
    created() {
        this.timer = setInterval(() => {
            this.initTable();
            this.initChart();
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