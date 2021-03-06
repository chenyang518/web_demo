<template>
  <div :id="className" :style="{height:height,width:width}" ></div>
</template>

<script>

import * as echarts from 'echarts'

export default {
    props: {
        className: {
            type: String,
            default: 'chart'
        },
        width: {
            type: String,
            default: '100%'
        },
        height: {
            type: String,
            default: '350px'
        },
        chartData: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            chart: null
        }
    },
    watch: {
        chartData: {
            deep:true,
            handler(newVal,oldVal) {
                if (newVal) 
                    this.setOptions(newVal);
                else
                    this.setOptions(oldVal);
            }
        }
    },
    mounted() {
        this.$nextTick(() => {
            this.initChart()
        })
    },
    beforeDestroy() {
        if (!this.chart)
            return
        this.chart.dispose()
        this.chart = null
    },
    methods: {
        initChart() {
            this.chart = echarts.init(this.$el)
            this.setOptions(this.chartData)
        },
        setOptions({months,data1,data2} = {}) {
            this.chart.setOption({
                tooltip: {
                    trigger: "axis",
                    axisPointer: {
                        type: "shadow",
                        label: {
                            show: true
                        }
                    }
                },
                xAxis: [{
                    type: 'category',
                    data: months,
                    axisLine: {
                        show: true
                    },
                    axisTick: {
                        show: false
                    },
                    axisLabel: {
                        show: true,
                        textStyle: {
                            color: "#FFFFFF",
                        }
                    }
                }],
                legend: {
                    data: ['Actual','Plan'],
                    textStyle: {
                        color: '#FFFFFF'
                    },
                },
                yAxis: [{
                    type: 'value',
                    splitLine: {
                        show: false
                    },
                    axisLine: {
                        lineStyle: {
                            color: "#FFFFFF",
                        }
                    }
                }],
                series: [{
                    name: 'Actual',
                    type: 'bar',
                    barWidth: 15,
                    data: data1,
                    itemStyle: {
                        normal: {
                            color: new echarts.graphic.LinearGradient(0,0,0,1, [{
                                offset: 0,
                                color: "#00FFE3"
                            },
                            {
                                offset: 1,
                                color: "#4693EC"
                            }])
                        }
                    },
                    label: {
                        show: true,
                        position: 'top'
                    }
                },
                {
                    name: 'Plan',
                    type: 'line',
                    data: data2,
                    smooth: true,
                    symbol: "circle",
                    symbolSize: 10,
                    itemStyle: {
                        color: "#058CFF"
                    },
                    lineStyle: {
                        color: "#058CFF"
                    },
                    areaStyle: {
                        color: "rgba(5,144,255,0.2)"
                    },
                    label: {
                        show: true,
                        position: 'bottom',
                        distance: 5,
                    }
                }]
            })
        }
    },
}
</script>

<style>

</style>