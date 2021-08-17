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
import MyChart from '../components/MyChart';
import Card from '../components/Cards/Card.vue';
import axios from 'axios'

const tableColumns = ["Name", "Country", "City", "Salary"];
const tableData = [
  {
    id: 1,
    name: "Dakota Rice",
    salary: "$36.738",
    country: "Niger",
    city: "Oud-Turnhout",
  },
  {
    id: 2,
    name: "Minerva Hooper",
    salary: "$23,789",
    country: "Curaçao",
    city: "Sinaai-Waas"
  },
  {
    id: 3,
    name: "Sage Rodriguez",
    salary: "$56,142",
    country: "Netherlands",
    city: "Baileux"
  },
  {
    id: 4,
    name: "Philip Chaney",
    salary: "$38,735",
    country: "Korea, South",
    city: "Overland Park"
  },
  {
    id: 5,
    name: "Doris Greene",
    salary: "$63,542",
    country: "Malawi",
    city: "Feldkirchen in Kärnten"
  },
  {
    id: 6,
    name: 'Mason Porter',
    salary: '$98,615',
    country: 'Chile',
    city: 'Gloucester'
  },
  {
    id: 7,
    name: 'Jon Porter',
    salary: '$78,615',
    country: 'Portugal',
    city: 'Gloucester'
  }
];

export default {
    components: {
      BaseTable,
      MyChart,
      Card,
    },
    data() {
      return {
        table2: {
            columns : [],
            data: [],
        },
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
        }
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
        return this.$t('dashboard.chartCategories');
      },
    },
    watch: {

    },
    methods: {
        initChart(index) {
            const path = 'http://localhost:5000/labor-reduction';
            axios.get(path)
                .then((res) => {
                    
                    this.myChart.chartData.data1 = [];
                    this.myChart.chartData.data2 = [];
                    this.myChart.activeIndex = index;
                    index = (this.$t('dashboard.chartCategories'))[index] + " Actual";
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
                    this.table.columns =['Headcount','Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                    var k = 1;
                    var data = [];
                    for (var i in res.data) {
                        var temp = {
                            id: k++, Headcount: res.data[i]['Headcount'],
                            Jan: res.data[i]['Jan'], Feb: res.data[i]['Feb'], Mar: res.data[i]['Mar'], Apr: res.data[i]['Apr'],
                            May: res.data[i]['May'], Jun: res.data[i]['Jun'], Jul: res.data[i]['Jul'], Aug: res.data[i]['Aug'],
                            Sep: res.data[i]['Sep'], Oct: res.data[i]['Oct'], Nov: res.data[i]['Nov'], Dec: res.data[i]['Dec'], 
                        };
                        data.push(temp);
                        console.log(typeof(temp));
                    }
                    console.log(data);
                    console.log(tableData);
                    console.log(typeof(data));
                    console.log(typeof(tableData));
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
      
    },
    created() {
        this.initTable();
    },
    beforeDestroy() {
      if (this.$rtl.isRTL) {
        this.i18n.locale = 'en';
        this.$rtl.disableRTL();
      }
    }
};
</script>

<style>

</style>