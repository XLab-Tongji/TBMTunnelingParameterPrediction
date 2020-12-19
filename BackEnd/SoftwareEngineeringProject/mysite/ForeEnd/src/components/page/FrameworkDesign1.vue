<template>

    <div class="container">

        <div id="contrast" class="frameContrast">
            <div class="h1title" style="background: #00d1b2;margin-top: 20px">比对模型</div>
            <div style="margin-left: 30px">

                <el-card shadow="hover" class="mgb20" >
                    <div class="block" >
                        <div style="float: left;width: 250px;height: 250px;margin-right: 30px">
                            <el-image
                                style="width: 250px; height: 250px; border-radius: 50%;background: white"
                                :src="imgs2"
                                :preview-src-list="imgs2"
                                :fit="fit"
                            >
                            </el-image>
                        </div>
                        <div class="labeltitle" >比对模型1：为了对LA的预测结果进行比对分析</div>

                    </div>
                </el-card>

                <el-card shadow="hover" class="mgb20">
                    <div class="block" >
                        <div style="float: left;width: 250px;height: 250px;margin-right: 30px">
                            <el-image
                                style="width: 250px; height: 250px; border-radius: 50%; background: white"
                                :src="imgs1"
                                :preview-src-list="imgs1"
                                :fit="fit"
                            >
                            </el-image>
                        </div>
                        <div class="labeltitle" >比对模型2:对Tree结构的NN预测效果进行比对分析</div>

                    </div>
                </el-card>

            </div>
        </div>

        <div id="testData" class="frameContrast">

            <div class="h1title">测试数据</div>

            <div style="width: 700px;padding-left: 40px;padding-top: 20px;
            margin-top:20px;background:#c7ddef;float: left;">
                <el-table
                    :data="TableData"
                    stripe
                    style="width: 100%"
                    border
                >
                    <el-table-column
                        v-for="info in TestHeader" :key="info.key"
                        :width="125"
                        :property="info.key"
                        :label="info.label"
                    >
                        <template slot-scope="scope">
                            {{scope.row[scope.column.property]}}
                        </template>
                    </el-table-column>
                </el-table>
            </div>

            <div style="width: 280px;margin-left:20px;padding-top:20px;
            margin-top:20px;background:#c7ddef;float: left;">
                <el-table
                    :data="TableData1"
                    stripe
                    style="width: 100%"
                    border
                >
                    <el-table-column
                        v-for="info in TestHeader1" :key="info.key"
                        :property="info.key"
                        :label="info.label"
                    >
                        <template slot-scope="scope">
                            {{scope.row[scope.column.property]}}
                        </template>
                    </el-table-column>
                </el-table>
            </div>

            <div style="width: 800px;height: 80px;margin-top:570px;background:#c7ddef;float: none;">
                <el-button type="primary" icon="el-icon-refresh" @click="NewSample" style="margin-left: 500px">换一批</el-button>
                <el-button type="primary" @click="TestResult" style="margin-left: 100px">测试<i class="el-icon-orange el-icon--right"></i></el-button>
            </div>

            <div class="h1title">测试结果</div>

            <div id="echart1" style="width: 1000px;height: 600px;padding-top:50px;margin-left: 50px;"></div>
        </div>

        <div id=testResult class="frameContrast">

            <div id="echart2" style="width: 1000px;height: 600px;padding-top:50px;margin-left: 50px;"></div>
            <div id="echart3" style="width: 1000px;height: 600px;padding-top:50px;margin-left: 50px;"></div>
            <div id="echart4" style="width: 1000px;height: 600px;padding-top:50px;margin-left: 50px;"></div>

        </div>

        <div id="testResultIndex" class="frameContrast">
            <div class="h1title">测试结果分析指标</div>
            <div style="width: 300px;margin-left: 40px;padding-top: 20px">
                <el-table :data="Result" stripe style="width: 100%">
                    <el-table-column prop="R2" label="R2" width="100">
                    </el-table-column>
                    <el-table-column prop="RMSE" label="RMSE" width="100">
                    </el-table-column>
                    <el-table-column prop="MAE"  label="MAE" width="100">
                    </el-table-column>
                </el-table>
            </div>

        </div>

    </div>
</template>


<script>
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min";
let xAxisData = [];
let data1_1 = [15713.91974,
    16015.02828,
    15891.69147,
    16218.16112,
    16051.47614,
    18342.42524,
    17358.14431,
    12261.25375,
    16975.58267,
    17423.11741,];
let data1_2=[2942.392641,
    3013.518114,
    3179.002699,
    3119.361978,
    3172.595804,
    3013.220918,
    2657.163266,
    1370.768179,
    3200.057552,
    3066.926265
];
let data1_3=[60.83314267,
    67.05818797,
    73.1904141,
    69.30692463,
    69.89331471,
    66.58043495,
    63.93757212,
    32.26763359,
    70.48208008,
    65.59021875,
];
let data2_1 = [16766.57589,
    17273.52,
    17295.50119,
    16779.34071,
    16851.55698,
    15933.31996,
    12091.37486,
    16497.43053,
    16799.43102,
    15059.08978,
];
let data2_2=[2762.575388,
    2401.740375,
    2537.502591,
    2496.993468,
    2486.013825,
    2855.320806,
    1487.854634,
    2079.444166,
    2526.25951,
    2648.677084
];
let data2_3=[58.67710079,
    51.94760561,
    55.47151693,
    55.26619018,
    57.09060059,
    66.19874308,
    35.57291592,
    47.00089018,
    56.35334369,
    62.03316365,
];

for (let i = 1; i <= 10; i++) {
    xAxisData.push('组' + i);
}

export default {
    baseURL: 'http://localhost:8080',
    name: 'FrameworkDesign',

    data() {
        return {
            fit: 'scale-down',
            option: {
                title: {
                    text: '稳定段总推进力'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['原数据', '预测结果']
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: ['组1', '组2', '组3', '组4', '组5', '组6', '组7', '组8', '组9', '组10']
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '原数据',
                        type: 'line',
                        stack: '总量',
                        data: [15713.91974,
                            16015.02828,
                            15891.69147,
                            16218.16112,
                            16051.47614,
                            18342.42524,
                            17358.14431,
                            12261.25375,
                            16975.58267,
                            17423.11741]
                    },
                    {
                        name: '预测结果',
                        type: 'line',
                        stack: '总量',
                        data: [16766.57589,
                            17273.52,
                            17295.50119,
                            16779.34071,
                            16851.55698,
                            15933.31996,
                            12091.37486,
                            16497.43053,
                            16799.43102,
                            15059.08978]
                    },

                ]
            },

            option1: {
                legend: {},
                tooltip: {},
                dataset: {
                    source: [
                        ['dataset', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                        ['稳定段总推进力均值/4', 15713.91974 / 4, 15713.91974 / 4, 15713.91974 / 4, 15713.91974 / 4, 15713.91974 / 4, 15713.91974 / 4, 15713.91974 / 4, 15713.91974 / 4, 15713.91974 / 4, 15713.91974 / 4,],
                        ['稳定段刀盘扭矩均值', 2942.392641, 2942.392641, 2942.392641, 2942.392641, 2942.392641, 2942.392641, 2942.392641, 2942.392641, 2942.392641, 2942.392641,],
                        ['稳定段推进速度均值*40', 60.83314267 * 40, 60.83314267 * 40, 60.83314267 * 40, 60.83314267 * 40, 60.83314267 * 40, 60.83314267 * 40, 60.83314267 * 40, 60.83314267 * 40, 60.83314267 * 40, 60.83314267 * 40,]
                    ]
                },

                xAxis: [
                    { type: 'category', gridIndex: 0 },
                ],
                yAxis: [
                    { gridIndex: 0 },
                ],
                grid: [
                    { top: '15%' }
                ],
                series: [
                    // {name:['稳定段总推进力均值','稳定段刀盘扭矩均值','稳定段推进速度均值']},
                    // These series are in the first grid.
                    { type: 'bar', seriesLayoutBy: 'row' },
                    { type: 'bar', seriesLayoutBy: 'row' },
                    { type: 'bar', seriesLayoutBy: 'row' },
                ]
            },

            // option2:{
            //     title: {
            //         text: '稳定段总推进力'
            //     },
            //     legend: {
            //         data: [
            //             {
            //                 name:'原数据',
            //                 textStyle:{color:'#61a0a8'}
            //             },
            //             {
            //                 name:'结果',
            //                 textStyle:{color:'#d48265'}
            //             }
            //             ]
            //     },
            //     toolbox: {
            //         // y: 'bottom',
            //         feature: {
            //             magicType: {
            //                 type: ['stack', 'tiled']
            //             },
            //             dataView: {},
            //             saveAsImage: {
            //                 pixelRatio: 2
            //             }
            //         }
            //     },
            //     tooltip: {},
            //     xAxis: {
            //         data: xAxisData,
            //         splitLine: {
            //             show: false
            //         }
            //     },
            //     yAxis: {
            //     },
            //
            //
            //     series: [{
            //         name: '原数据',
            //         type: 'bar',
            //         data: data1_1,
            //         color:'#61a0a8',
            //         // itemStyle: {
            //         //     normal: {
            //         //         //这里是重点
            //         //         color: function(params) {
            //         //             //注意，如果颜色太少的话，后面颜色不会自动循环，最好多定义几个颜色
            //         //             var colorList = ['#61a0a8', '#d48265', '#91c7ae','#749f83', '#ca8622'];
            //         //             return colorList[params.dataIndex]
            //         //         }
            //         //     }
            //         // },
            //
            //         animationDelay: function (idx) {
            //             return idx * 10;
            //         }
            //     }, {
            //         name: '结果',
            //         type: 'bar',
            //         data: data2_1,
            //         color:'#d48265',
            //         animationDelay: function (idx) {
            //             return idx * 10 + 100;
            //         }
            //     }],
            //     animationEasing: 'elasticOut',
            //     animationDelayUpdate: function (idx) {
            //         return idx * 5;
            //     }
            // },
            //
            // option3:{
            //     title: {
            //         text: '稳定段刀盘扭矩均值'
            //     },
            //     legend: {
            //         data: ['原数据', '结果']
            //     },
            //     toolbox: {
            //         // y: 'bottom',
            //         feature: {
            //             magicType: {
            //                 type: ['stack', 'tiled']
            //             },
            //             dataView: {},
            //             saveAsImage: {
            //                 pixelRatio: 2
            //             }
            //         }
            //     },
            //     tooltip: {},
            //     xAxis: {
            //         data: xAxisData,
            //         splitLine: {
            //             show: false
            //         }
            //     },
            //     yAxis: {
            //     },
            //     itemStyle: {
            //         normal: {
            //             //这里是重点
            //             color: function(params) {
            //                 //注意，如果颜色太少的话，后面颜色不会自动循环，最好多定义几个颜色
            //                 var colorList = [, '#91c7ae','#749f83', '#ca8622','#61a0a8', '#d48265'];
            //                 return colorList[params.dataIndex]
            //             }
            //         }
            //     },
            //     series: [{
            //         name: '原数据',
            //         type: 'bar',
            //         data: data1_2,
            //         animationDelay: function (idx) {
            //             return idx * 10;
            //         }
            //     }, {
            //         name: '结果',
            //         type: 'bar',
            //         data: data2_2,
            //         animationDelay: function (idx) {
            //             return idx * 10 + 100;
            //         }
            //     }],
            //     animationEasing: 'elasticOut',
            //     animationDelayUpdate: function (idx) {
            //         return idx * 5;
            //     }
            // },
            //
            // option4:{
            //     title: {
            //         text: '稳定段推进速度均值'
            //     },
            //     legend: {
            //         data: ['原数据', '结果']
            //     },
            //     toolbox: {
            //         // y: 'bottom',
            //         feature: {
            //             magicType: {
            //                 type: ['stack', 'tiled']
            //             },
            //             dataView: {},
            //             saveAsImage: {
            //                 pixelRatio: 2
            //             }
            //         }
            //     },
            //     tooltip: {},
            //     xAxis: {
            //         data: xAxisData,
            //         splitLine: {
            //             show: false
            //         }
            //     },
            //     yAxis: {
            //     },
            //     itemStyle: {
            //         normal: {
            //             //这里是重点
            //             color: function(params) {
            //                 //注意，如果颜色太少的话，后面颜色不会自动循环，最好多定义几个颜色
            //                 let colorList = [ '#ca8622','#61a0a8', '#d48265','#91c7ae','#749f83'];
            //                 return colorList[params.dataIndex]
            //             }
            //         }
            //     },
            //     series: [{
            //         name: '原数据',
            //         type: 'bar',
            //         data: data1_3,
            //         color:'#ca8622',
            //         // itemStyle: {
            //         //     normal: {
            //         //         //这里是重点
            //         //         color: function(params) {
            //         //             //注意，如果颜色太少的话，后面颜色不会自动循环，最好多定义几个颜色
            //         //             let colorList = [ '#ca8622','#61a0a8', '#d48265','#91c7ae','#749f83'];
            //         //             return colorList[params.dataIndex]
            //         //         }
            //         //     }
            //         // },
            //         animationDelay: function (idx) {
            //             return idx * 10;
            //         }
            //     }, {
            //         name: '结果',
            //         type: 'bar',
            //         data: data2_3,
            //         color:'#749f83',
            //         // itemStyle: {
            //         //     normal: {
            //         //         //这里是重点
            //         //         color: function(params) {
            //         //             //注意，如果颜色太少的话，后面颜色不会自动循环，最好多定义几个颜色
            //         //             let colorList = [ '#d48265','#91c7ae','#749f83','#ca8622','#61a0a8'];
            //         //             return colorList[params.dataIndex]
            //         //         }
            //         //     }
            //         // },
            //         animationDelay: function (idx) {
            //             return idx * 10 + 100;
            //         }
            //     }],
            //     animationEasing: 'elasticOut',
            //     animationDelayUpdate: function (idx) {
            //         return idx * 5;
            //     }
            // },

            option2: {

                title: {
                    text: '稳定段总推进力'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['原数据', '预测结果']
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: ['组1', '组2', '组3', '组4', '组5', '组6', '组7', '组8', '组9', '组10']
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '原数据',
                        type: 'line',
                        stack: '总量',
                        data: data1_1
                    },
                    {
                        name: '预测结果',
                        type: 'line',
                        stack: '总量',
                        data: data2_1
                    },

                ]
            },

            option3: {

                title: {
                    text: '稳定段总推进力'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['原数据', '预测结果']
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: ['组1', '组2', '组3', '组4', '组5', '组6', '组7', '组8', '组9', '组10']
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '原数据',
                        type: 'line',
                        stack: '总量',
                        data: data1_2
                    },
                    {
                        name: '预测结果',
                        type: 'line',
                        stack: '总量',
                        data: data2_2
                    },
                ]
            },

            option4: {

                title: {
                    text: '稳定段总推进力'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['原数据', '预测结果']
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: ['组1', '组2', '组3', '组4', '组5', '组6', '组7', '组8', '组9', '组10']
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '原数据',
                        type: 'line',
                        stack: '总量',
                        data: data1_3
                    },
                    {
                        name: '预测结果',
                        type: 'line',
                        stack: '总量',
                        data: data2_3
                    },

                ]
            },

            TableData: [
                {
                    a: "302.53231",
                    b: "0.722609417",
                    c: "7.00694437",
                    d: "7.51E-06",
                    e: "44.57949944",
                    f: "0.085447488",
                    g: "1504.349398",
                    h: "68422.44789",
                    i: "1108.1",
                    j: "37180.52414",
                    k: "177.8853195",
                    l: "137.1489792",
                    m: "4.814581641",
                    n: "0.700421557",
                    o: "13971.11312",
                    p: "846007.9146",
                    q: "33.88139648",
                    r: "36.11885989",
                    s: "142.2444509",
                    t: "27.57576434",
                    u: "3.350141072",
                    v: "6.40E-06",
                    w: "2.671452014",
                    x: "2.09E-07",
                    y: "2.754804826",
                    z: "3.04E-05",
                    aa: "15713.91974",
                    ab: "2942.392641",
                    ac: "60.83314267"
                },
                {
                    a: "302.53231",
                    b: "0.722609417",
                    c: "7.00694437",
                    d: "7.51E-06",
                    e: "44.57949944",
                    f: "0.085447488",
                    g: "1504.349398",
                    h: "68422.44789",
                    i: "1108.1",
                    j: "37180.52414",
                    k: "177.8853195",
                    l: "137.1489792",
                    m: "4.814581641",
                    n: "0.700421557",
                    o: "13971.11312",
                    p: "846007.9146",
                    q: "33.88139648",
                    r: "36.11885989",
                    s: "142.2444509",
                    t: "27.57576434",
                    u: "3.350141072",
                    v: "6.40E-06",
                    w: "2.671452014",
                    x: "2.09E-07",
                    y: "2.754804826",
                    z: "3.04E-05",
                    aa: "15713.91974",
                    ab: "2942.392641",
                    ac: "60.83314267"
                },
                {
                    a: "302.53231",
                    b: "0.722609417",
                    c: "7.00694437",
                    d: "7.51E-06",
                    e: "44.57949944",
                    f: "0.085447488",
                    g: "1504.349398",
                    h: "68422.44789",
                    i: "1108.1",
                    j: "37180.52414",
                    k: "177.8853195",
                    l: "137.1489792",
                    m: "4.814581641",
                    n: "0.700421557",
                    o: "13971.11312",
                    p: "846007.9146",
                    q: "33.88139648",
                    r: "36.11885989",
                    s: "142.2444509",
                    t: "27.57576434",
                    u: "3.350141072",
                    v: "6.40E-06",
                    w: "2.671452014",
                    x: "2.09E-07",
                    y: "2.754804826",
                    z: "3.04E-05",
                    aa: "15713.91974",
                    ab: "2942.392641",
                    ac: "60.83314267"
                },
                {
                    a: "302.53231",
                    b: "0.722609417",
                    c: "7.00694437",
                    d: "7.51E-06",
                    e: "44.57949944",
                    f: "0.085447488",
                    g: "1504.349398",
                    h: "68422.44789",
                    i: "1108.1",
                    j: "37180.52414",
                    k: "177.8853195",
                    l: "137.1489792",
                    m: "4.814581641",
                    n: "0.700421557",
                    o: "13971.11312",
                    p: "846007.9146",
                    q: "33.88139648",
                    r: "36.11885989",
                    s: "142.2444509",
                    t: "27.57576434",
                    u: "3.350141072",
                    v: "6.40E-06",
                    w: "2.671452014",
                    x: "2.09E-07",
                    y: "2.754804826",
                    z: "3.04E-05",
                    aa: "15713.91974",
                    ab: "2942.392641",
                    ac: "60.83314267"
                },
                {
                    a: "302.53231",
                    b: "0.722609417",
                    c: "7.00694437",
                    d: "7.51E-06",
                    e: "44.57949944",
                    f: "0.085447488",
                    g: "1504.349398",
                    h: "68422.44789",
                    i: "1108.1",
                    j: "37180.52414",
                    k: "177.8853195",
                    l: "137.1489792",
                    m: "4.814581641",
                    n: "0.700421557",
                    o: "13971.11312",
                    p: "846007.9146",
                    q: "33.88139648",
                    r: "36.11885989",
                    s: "142.2444509",
                    t: "27.57576434",
                    u: "3.350141072",
                    v: "6.40E-06",
                    w: "2.671452014",
                    x: "2.09E-07",
                    y: "2.754804826",
                    z: "3.04E-05",
                    aa: "15713.91974",
                    ab: "2942.392641",
                    ac: "60.83314267"
                },
                {
                    a: "302.53231",
                    b: "0.722609417",
                    c: "7.00694437",
                    d: "7.51E-06",
                    e: "44.57949944",
                    f: "0.085447488",
                    g: "1504.349398",
                    h: "68422.44789",
                    i: "1108.1",
                    j: "37180.52414",
                    k: "177.8853195",
                    l: "137.1489792",
                    m: "4.814581641",
                    n: "0.700421557",
                    o: "13971.11312",
                    p: "846007.9146",
                    q: "33.88139648",
                    r: "36.11885989",
                    s: "142.2444509",
                    t: "27.57576434",
                    u: "3.350141072",
                    v: "6.40E-06",
                    w: "2.671452014",
                    x: "2.09E-07",
                    y: "2.754804826",
                    z: "3.04E-05",
                    aa: "15713.91974",
                    ab: "2942.392641",
                    ac: "60.83314267"
                },
                {
                    a: "302.53231",
                    b: "0.722609417",
                    c: "7.00694437",
                    d: "7.51E-06",
                    e: "44.57949944",
                    f: "0.085447488",
                    g: "1504.349398",
                    h: "68422.44789",
                    i: "1108.1",
                    j: "37180.52414",
                    k: "177.8853195",
                    l: "137.1489792",
                    m: "4.814581641",
                    n: "0.700421557",
                    o: "13971.11312",
                    p: "846007.9146",
                    q: "33.88139648",
                    r: "36.11885989",
                    s: "142.2444509",
                    t: "27.57576434",
                    u: "3.350141072",
                    v: "6.40E-06",
                    w: "2.671452014",
                    x: "2.09E-07",
                    y: "2.754804826",
                    z: "3.04E-05",
                    aa: "15713.91974",
                    ab: "2942.392641",
                    ac: "60.83314267"
                },
                {
                    a: "302.53231",
                    b: "0.722609417",
                    c: "7.00694437",
                    d: "7.51E-06",
                    e: "44.57949944",
                    f: "0.085447488",
                    g: "1504.349398",
                    h: "68422.44789",
                    i: "1108.1",
                    j: "37180.52414",
                    k: "177.8853195",
                    l: "137.1489792",
                    m: "4.814581641",
                    n: "0.700421557",
                    o: "13971.11312",
                    p: "846007.9146",
                    q: "33.88139648",
                    r: "36.11885989",
                    s: "142.2444509",
                    t: "27.57576434",
                    u: "3.350141072",
                    v: "6.40E-06",
                    w: "2.671452014",
                    x: "2.09E-07",
                    y: "2.754804826",
                    z: "3.04E-05",
                    aa: "15713.91974",
                    ab: "2942.392641",
                    ac: "60.83314267"
                },
                {
                    a: "302.53231",
                    b: "0.722609417",
                    c: "7.00694437",
                    d: "7.51E-06",
                    e: "44.57949944",
                    f: "0.085447488",
                    g: "1504.349398",
                    h: "68422.44789",
                    i: "1108.1",
                    j: "37180.52414",
                    k: "177.8853195",
                    l: "137.1489792",
                    m: "4.814581641",
                    n: "0.700421557",
                    o: "13971.11312",
                    p: "846007.9146",
                    q: "33.88139648",
                    r: "36.11885989",
                    s: "142.2444509",
                    t: "27.57576434",
                    u: "3.350141072",
                    v: "6.40E-06",
                    w: "2.671452014",
                    x: "2.09E-07",
                    y: "2.754804826",
                    z: "3.04E-05",
                    aa: "15713.91974",
                    ab: "2942.392641",
                    ac: "60.83314267"
                },
                {
                    a: "302.53231",
                    b: "0.722609417",
                    c: "7.00694437",
                    d: "7.51E-06",
                    e: "44.57949944",
                    f: "0.085447488",
                    g: "1504.349398",
                    h: "68422.44789",
                    i: "1108.1",
                    j: "37180.52414",
                    k: "177.8853195",
                    l: "137.1489792",
                    m: "4.814581641",
                    n: "0.700421557",
                    o: "13971.11312",
                    p: "846007.9146",
                    q: "33.88139648",
                    r: "36.11885989",
                    s: "142.2444509",
                    t: "27.57576434",
                    u: "3.350141072",
                    v: "6.40E-06",
                    w: "2.671452014",
                    x: "2.09E-07",
                    y: "2.754804826",
                    z: "3.04E-05",
                    aa: "15713.91974",
                    ab: "2942.392641",
                    ac: "60.83314267"
                },

                // {a:309.4555359	b:0.100175663	c:7.028488191
                // d:1.05E-05	e:48.8787618	f:0.032418063	g:1517.904399	h:165850.5213	i:1121.75	j:90421.68534	k:173.6482447	l:183.2905059	m:5.20246795	n:1.760681307	o:13638.3333
                // p:1130633.471	q:36.56394043	r:86.84246076	s:362.2314168	t:35.287921	    u:3.344800091	v:2.57E-05	w:2.671141418	x:1.88E-07	y:2.754297702	z:3.17E-05
                // aa:16015.02828	ab:3013.518114	ac:67.05818797},
                // {a:305.6018483	b:0.243127045	c:4.970281394
                // d:0.093314109	e:45.34223137	f:0.003296093	g:856.2925883	h:133785.4725	i:455	j:47170.10345	k:124.9329666	l:808.3214782	m:5.310096788	n:1.185727967	o:9812.235286
                // p:4986156.524	q:26.45834961	r:34.53270376	s:94.9226237	t:16.92218613	u:3.250398882	v:0.000661013	w:2.672982176	x:1.48E-07	y:2.756069517	z:3.72E-05
                // aa:15891.69147	ab:3179.002699	ac:73.1904141},
                // a:303.1274119	b:0.906764907	c:5.341820574
                // d:0.204697395	e:45.00173581	f:0.002789098	g:1031.946	h:153288.6609	i:589.9833333	j:67650.99109	k:141.7925339	l:511.9884659	m:5.215185571	n:0.671760299	o:11136.38569
                // p:3158217.069	q:27.92825928	r:27.77185818	s:114.751061	t:19.0707756	u:3.243413552	v:0.001246344	w:2.672307849	x:1.17E-07	y:2.754524493	z:3.30E-05
                // aa:16218.16112	ab:3119.361978	ac:69.30692463
                // a:303.0936564	b:0.09766852	c:6.897054879
                // d:3.34E-05	e:48.26367188	f:0.018620891	g:2839.023092	h:324781.525	i:2058.583333	j:170193.967	k:191.9232244	l:291.9906878	m:10.08673391	n:1.888248156	o:15073.6502
                // p:1801153.883	q:69.56325684	r:89.12710206	s:310.0466349	t:112.6302245	u:3.200111604	v:0.000215051	w:2.671156629	x:9.24E-08	y:2.752615476	z:4.12E-05
                // aa:16051.47614	ab:3172.595804	ac:69.89331471
                // a:298.0348185	b:4.336870015	c:6.805638774
                // d:3.79E-05	e:48.29448764	f:0.000274559	g:1546.221094	h:349835.8559	i:1104.833333	j:178647.523	k:186.5909536	l:767.4769479	m:6.075668804	n:2.329215423	o:14654.85368
                // p:4734206.139	q:41.3411377	r:107.2662551	s:163.4570546	t:43.51274065	u:2.945725989	v:0.000189745	w:2.671755028	x:7.37E-08	y:2.755067285	z:3.34E-05
                // aa:18342.42524	ab:3013.220918	ac:66.58043495
                // a:301.2374613	b:0.936832494	c:7.010385418
                // d:8.49E-05	e:48.17035586	f:0.006288837	g:2191.527584	h:112187.536	i:1615.016667	j:62092.02557	k:206.3208913	l:82.17921312	m:7.395469554	n:1.192370527	o:16204.44307
                // p:506925.1459	q:51.85096436	r:59.3000547	s:133.2443329	t:62.53347349	u:3.328995204	v:0.000271358	w:2.671550536	x:4.39E-08	y:2.756188814	z:3.39E-05
                // aa:17358.14431	ab:2657.163266	ac:63.93757212
                // a:331.0194834	b:0.000879628	c:5.605534347
                // d:0.32802752	e:44.57219315	f:0.004632794	g:250.7810354	h:10256.44736	i:140.5833333	j:1767.449713	k:0.201099538	l:0.000596898	m:0.204219833	n:0.056525371	o:15.79435803
                // p:3.681982735	q:1.212561035	r:2.124297094	s:47.06181844	t:0.002172511	u:3.288464793	v:0.00014476	w:2.682049561	x:4.17E-08	y:2.757298438	z:3.38E-05
                // aa:12261.25375	ab:1370.768179	ac:32.26763359
                // a:323.1727437	b:0.988521539	c:3.472453229
                // d:2.218166562	e:44.88375282	f:0.088702937	g:343.5049021	h:1281.282486	i:122.0333333	j:3058.050575	k:35.21604897	l:574.185468	m:5.444280247	n:58.60132322	o:2591.373033
                // p:4403935.026	q:28.44273682	r:1813.919187	s:42.03963928	t:40.02251086	u:3.303772799	v:0.000127522	w:2.682276726	x:6.31E-08	y:2.758061989	z:3.46E-05
                // aa:16975.58267	ab:3200.057552	ac:70.48208008
                // a:324.7535706	b:0.051352176	c:6.410623821
                // d:1.27E-05	e:50.33774605	f:0.135726225	g:1436.069419	h:87026.80087	i:967.8666667	j:38784.96437	k:163.3318863	l:147.1976805	m:5.979291765	n:1.229931823	o:12828.08646
                // p:907993.4818	q:38.32781982	r:50.34760717	s:101.1697266	t:54.74128674	u:3.302249622	v:8.78E-05	w:2.678292338	x:5.82E-08	y:2.757578786	z:3.16E-05
                // aa:17423.11741	ab:3066.926265	ac:65.59021875
            ],

            TestHeader: [
                { key: "a", label: "上升段撑靴压力均值" },

                { key: "b", label: "上升段撑靴压力方差" },

                { key: "c", label: "上升段刀盘转速均值" },

                { key: "d", label: "上升段刀盘转速方差" },

                { key: "e", label: "上升段刀盘刹车压力均值" },

                { key: "f", label: "上升段刀盘刹车压力方差" },

                { key: "g", label: "上升段刀盘扭矩均值" },

                { key: "h", label: "上升段刀盘扭矩方差" },

                { key: "i", label: "上升段刀盘功率均值" },

                { key: "j", label: "上升段刀盘功率方差" },

                { key: "k", label: "上升段推进压力均值" },

                { key: "l", label: "上升段推进压力方差" },

                { key: "m", label: "上升段贯入度均值" },

                { key: "n", label: "上升段贯入度方差" },

                { key: "o", label: "上升段总推进力均值" },

                { key: "p", label: "上升段总推进力方差" },

                { key: "q", label: "上升段推进速度均值" },

                { key: "r", label: "上升段推进速度方差" },

                { key: "s", label: "上升段推进位移均值" },

                { key: "t", label: "上升段推进位移方差" },

                { key: "u", label: "上升段主机皮带机转速均值" },

                { key: "v", label: "上升段主机皮带机转速方差" },

                { key: "w", label: "上升段桥架皮带机转速均值" },

                { key: "x", label: "上升段桥架皮带机转速方差" },

                { key: "y", label: "上升段转渣皮带机转速均值" },

                { key: "z", label: "上升段转渣皮带机转速方差" },

                { key: "aa", label: "稳定段总推进力均值" },

                { key: "ab", label: "稳定段刀盘扭矩均值" },

                { key: "ac", label: "稳定段推进速度均值" }


            ],

            TableData1: [
                {
                    aa: "15713.91974", ab: "2942.392641", ac: "60.83314267"
                },
                {
                    aa: "15713.91974", ab: "2942.392641", ac: "60.83314267"
                },
                {
                    aa: "15713.91974", ab: "2942.392641", ac: "60.83314267"
                },
                {
                    aa: "15713.91974", ab: "2942.392641", ac: "60.83314267"
                },
                {
                    aa: "15713.91974", ab: "2942.392641", ac: "60.83314267"
                },
                {
                    aa: "15713.91974", ab: "2942.392641", ac: "60.83314267"
                },
                {
                    aa: "15713.91974", ab: "2942.392641", ac: "60.83314267"
                },
                {
                    aa: "15713.91974", ab: "2942.392641", ac: "60.83314267"
                },
                {
                    aa: "15713.91974", ab: "2942.392641", ac: "60.83314267"
                },
                {
                    aa: "15713.91974", ab: "2942.392641", ac: "60.83314267"
                },
                // {a:309.4555359	b:0.100175663	c:7.028488191
                // d:1.05E-05	e:48.8787618	f:0.032418063	g:1517.904399	h:165850.5213	i:1121.75	j:90421.68534	k:173.6482447	l:183.2905059	m:5.20246795	n:1.760681307	o:13638.3333
                // p:1130633.471	q:36.56394043	r:86.84246076	s:362.2314168	t:35.287921	    u:3.344800091	v:2.57E-05	w:2.671141418	x:1.88E-07	y:2.754297702	z:3.17E-05
                // aa:16015.02828	ab:3013.518114	ac:67.05818797},
                // {a:305.6018483	b:0.243127045	c:4.970281394
                // d:0.093314109	e:45.34223137	f:0.003296093	g:856.2925883	h:133785.4725	i:455	j:47170.10345	k:124.9329666	l:808.3214782	m:5.310096788	n:1.185727967	o:9812.235286
                // p:4986156.524	q:26.45834961	r:34.53270376	s:94.9226237	t:16.92218613	u:3.250398882	v:0.000661013	w:2.672982176	x:1.48E-07	y:2.756069517	z:3.72E-05
                // aa:15891.69147	ab:3179.002699	ac:73.1904141},
                // a:303.1274119	b:0.906764907	c:5.341820574
                // d:0.204697395	e:45.00173581	f:0.002789098	g:1031.946	h:153288.6609	i:589.9833333	j:67650.99109	k:141.7925339	l:511.9884659	m:5.215185571	n:0.671760299	o:11136.38569
                // p:3158217.069	q:27.92825928	r:27.77185818	s:114.751061	t:19.0707756	u:3.243413552	v:0.001246344	w:2.672307849	x:1.17E-07	y:2.754524493	z:3.30E-05
                // aa:16218.16112	ab:3119.361978	ac:69.30692463
                // a:303.0936564	b:0.09766852	c:6.897054879
                // d:3.34E-05	e:48.26367188	f:0.018620891	g:2839.023092	h:324781.525	i:2058.583333	j:170193.967	k:191.9232244	l:291.9906878	m:10.08673391	n:1.888248156	o:15073.6502
                // p:1801153.883	q:69.56325684	r:89.12710206	s:310.0466349	t:112.6302245	u:3.200111604	v:0.000215051	w:2.671156629	x:9.24E-08	y:2.752615476	z:4.12E-05
                // aa:16051.47614	ab:3172.595804	ac:69.89331471
                // a:298.0348185	b:4.336870015	c:6.805638774
                // d:3.79E-05	e:48.29448764	f:0.000274559	g:1546.221094	h:349835.8559	i:1104.833333	j:178647.523	k:186.5909536	l:767.4769479	m:6.075668804	n:2.329215423	o:14654.85368
                // p:4734206.139	q:41.3411377	r:107.2662551	s:163.4570546	t:43.51274065	u:2.945725989	v:0.000189745	w:2.671755028	x:7.37E-08	y:2.755067285	z:3.34E-05
                // aa:18342.42524	ab:3013.220918	ac:66.58043495
                // a:301.2374613	b:0.936832494	c:7.010385418
                // d:8.49E-05	e:48.17035586	f:0.006288837	g:2191.527584	h:112187.536	i:1615.016667	j:62092.02557	k:206.3208913	l:82.17921312	m:7.395469554	n:1.192370527	o:16204.44307
                // p:506925.1459	q:51.85096436	r:59.3000547	s:133.2443329	t:62.53347349	u:3.328995204	v:0.000271358	w:2.671550536	x:4.39E-08	y:2.756188814	z:3.39E-05
                // aa:17358.14431	ab:2657.163266	ac:63.93757212
                // a:331.0194834	b:0.000879628	c:5.605534347
                // d:0.32802752	e:44.57219315	f:0.004632794	g:250.7810354	h:10256.44736	i:140.5833333	j:1767.449713	k:0.201099538	l:0.000596898	m:0.204219833	n:0.056525371	o:15.79435803
                // p:3.681982735	q:1.212561035	r:2.124297094	s:47.06181844	t:0.002172511	u:3.288464793	v:0.00014476	w:2.682049561	x:4.17E-08	y:2.757298438	z:3.38E-05
                // aa:12261.25375	ab:1370.768179	ac:32.26763359
                // a:323.1727437	b:0.988521539	c:3.472453229
                // d:2.218166562	e:44.88375282	f:0.088702937	g:343.5049021	h:1281.282486	i:122.0333333	j:3058.050575	k:35.21604897	l:574.185468	m:5.444280247	n:58.60132322	o:2591.373033
                // p:4403935.026	q:28.44273682	r:1813.919187	s:42.03963928	t:40.02251086	u:3.303772799	v:0.000127522	w:2.682276726	x:6.31E-08	y:2.758061989	z:3.46E-05
                // aa:16975.58267	ab:3200.057552	ac:70.48208008
                // a:324.7535706	b:0.051352176	c:6.410623821
                // d:1.27E-05	e:50.33774605	f:0.135726225	g:1436.069419	h:87026.80087	i:967.8666667	j:38784.96437	k:163.3318863	l:147.1976805	m:5.979291765	n:1.229931823	o:12828.08646
                // p:907993.4818	q:38.32781982	r:50.34760717	s:101.1697266	t:54.74128674	u:3.302249622	v:8.78E-05	w:2.678292338	x:5.82E-08	y:2.757578786	z:3.16E-05
                // aa:17423.11741	ab:3066.926265	ac:65.59021875
            ],

            TestHeader1: [
                { key: "aa", label: "稳定段总推进力均值" },

                { key: "ab", label: "稳定段刀盘扭矩均值" },

                { key: "ac", label: "稳定段推进速度均值" }
            ],

            Result: [
                {
                    R2: "0",
                    RMSE: "0",
                    MAE: "0"
                },
                {
                    R2: "0",
                    RMSE: "0",
                    MAE: "0"
                }
            ],

            imgs1: require("@/assets/img/Tan2.png"),
            imgs2: require("@/assets/img/Tan3.png"),

            imgs3: require('@/assets/img/Loss1.png'),
            imgs4: require('@/assets/img/Loss2.png'),

        }
    },

    mounted() {
        let myChart1 = this.$echarts.init(document.getElementById('echart1'));
        let myChart2 = this.$echarts.init(document.getElementById('echart2'));
        let myChart3 = this.$echarts.init(document.getElementById('echart3'));
        let myChart4 = this.$echarts.init(document.getElementById('echart4'));

        myChart1.setOption(this.option1);
        myChart2.setOption(this.option);
        myChart3.setOption(this.option3);
        myChart4.setOption(this.option4);


        this.NewSample();
    },

    methods: {
        /**
         * 获取10个样例
         * 发送json包，区分稳定段标记为txt2和上升段标记为txt1
         */
        NewSample() {
            this.$http.get(this.publicPath + 'api/取得十个样例')
                .then(function(res) {
                    console.log(this.TableData1.aa.value());
                    console.log(this.TableData1.ab.value());
                    console.log(this.TableData1.ac.value());
                    // this.TableData = undefined;
                    // this.TableData = res.data.filter(l => l.type = "txt1");
                    // this.TableData1 = undefined;
                    // this.TableData1 = res.data.filter(l => l.type = "txt2");
                    //
                    // data2_1=this.TableData1.aa.value();
                    // data2_2=this.TableData1.ab.value();
                    // data2_3=this.TableData1.ac.value();
                })
                .catch()
            {
                console.log(this.TableData1.aa.value());
                console.log(this.TableData1.ab.value());
                console.log(this.TableData1.ac.value());
                console.error("后端获取样例失败")
            }
        },


        /**
         * 会向后端打包发送所有的测试数据，注意是一个对象数组，1~27列分别用字母a~z,az,ab,ac，请安顺序解析。
         * 默认调用LSTM的模型，（对比模型天老师还没搭）
         * 注意返回的json包含两大块内容，一个是三种稳定段的10组预测值，一个是对应模型的R2,MSE值
         * 两个大的json包前面加一个标签分别:R2,MSE标记为index.另外3*10的稳定段数值内部，对于同样含义的数组数据
         * 分别用result1,result2,result3标记区分
         */
        TestResult() {
            let temp1= JSON.stringify({"上升段数据":this.TableData,"稳定段数据":this.TableData1});
            this.$http.post(this.baseURL + 'api/模型测试数据', { temp1 })
                .then(function(res) {
                    this.Result = undefined;
                    this.Result = res.data.filter(l=>l.name="index");
                })
                .catch()
            {
                console.error("后端获取结果数据失败")
            }
        },
    },
}


</script>

<style scoped>


.frameContrast{
    width: 1100px;
    margin-bottom: 10px;
    background: #c7ddef;
}

.h1title{
    font-weight: bolder;
    margin-left: 20px;
    margin-bottom: 20px;
    margin-top: 10px;
    font-size: 30px;
    background: #c7ddef;
    border-top: 10px;
}

.el-card{
    margin-top: 20px;
    background: #c7ddef;
    height:350px;
    width: 1000px;
}

.block{
    height: 350px;
    margin-top: 20px;
    margin-left: 50px;
}

.labeltitle{
    float: left;
    font-size: 20px;
    line-height: 40px;
    text-align: center;
    height: 150px;
    width: 400px;
    color: #222222;
    background: #449d44;
    margin-top: 50px;
}

#contrast{
    background: #00d1b2;
    height: 850px;
}

#testData{
    background: #c7ddef;
}

#testResult{
    background: #c7ddef;
    height: 1800px;
}

#testResultIndex{
    background: #c7ddef;
    height: 700px;
}

</style>