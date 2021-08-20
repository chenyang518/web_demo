<template>
  <div>
    <div class="row">
      <div class="col-12">
        <card :title="table.title">
          <template slot="header">
            <div class="row">
              <div class="col-sm-6" :class="isRTL ? 'text-right' : 'text-left'">
                <h1 class="card-title">{{$t('dashboard.ciProject')}}</h1>
              </div>
              <div class="col-sm-6">
                <div class="btn-group btn-group-toggle"
                     :class="isRTL ? 'float-left' : 'float-right'"
                     data-toggle="buttons">
                  <label v-for="(option, index) in unitCategories"
                         :key="option"
                         class="btn btn-sm btn-primary btn-simple"
                         :class="{active: table.activeUnitIndex === index}"
                         :id="index">
                    <input type="radio"
                           @click="initTable(index, table.activeTimeIndex)"
                           name="options" autocomplete="off"
                           :checked="table.activeUnitIndex === index">
                    {{option}}
                  </label>
                </div>
              </div>
              <div class="col-sm-12">
                <div class="btn-group btn-group-toggle"
                     :class="isRTL ? 'float-left' : 'float-right'"
                     data-toggle="buttons">
                  <label v-for="(option, index) in timeCategories"
                         :key="option"
                         class="btn btn-sm btn-primary btn-simple"
                         :class="{active: table.activeTimeIndex === index}"
                         :id="index">
                    <input type="radio"
                           @click="initTable(table.activeUnitIndex, index)"
                           name="options" autocomplete="off"
                           :checked="table.activeTimeIndex === index">
                    {{option}}
                  </label>
                </div>
              </div>
            </div>
          </template>
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
import Card from '../components/Cards/Card.vue';
import axios from 'axios'

export default {
    components: {
      BaseTable,
      Card,
    },
    data() {
      return {
        table: {
          columns: [],
          data: [],
          activeUnitIndex: 4,
          activeTimeIndex: 0
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
      unitCategories() {
        return this.$t('dashboard.unitCategories');
      },
      timeCategories() {
        return this.$t('dashboard.timeCategories');
      },
    },
    methods: {
        initTable(unitIndex,timeIndex) {
            const path = 'http://localhost:5000/ci-project';
            axios.get(path)
                .then((res) => {
                    this.table.columns = [];
                    this.table.data = [];
                    this.table.activeUnitIndex = unitIndex;
                    unitIndex = (this.$t('dashboard.unitCategories'))[unitIndex];
                    this.table.activeTimeIndex = timeIndex;
                    timeIndex = (this.$t('dashboard.timeCategories'))[timeIndex];
                    this.table.columns =['No','CiNo','OpsUnit','CellNo','Desc En','Status','ActData','PPT Link','One Paper Link'];
                    var k = 1;
                    var data = [];
                    for (var i in res.data) {
                      if (unitIndex != 'Total' && res.data[i]['OpsUnit'] != unitIndex) 
                        continue;
                      if (res.data[i]['ActData'] != timeIndex)
                        continue;
                      var temp = {
                          id: k++, no: res.data[i]['No'], cino: res.data[i]['CiNo'], opsunit: res.data[i]['OpsUnit'],
                          cellno: res.data[i]['CellNo'], 'desc en': res.data[i]['Desc_En'], status: res.data[i]['Status'],
                          actdata: res.data[i]['ActData'], 
                          'ppt link': res.data[i]['PPT Link'], 
                          'one paper link': res.data[i]['One Paper Link']
                      };
                      console.log(typeof(temp['ppt link']));
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
      this.initTable(4,0);
    },
    created() {
        this.timer = setInterval(() => {
            this.initTable(this.table.activeUnitIndex, this.table.activeTimeIndex);
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