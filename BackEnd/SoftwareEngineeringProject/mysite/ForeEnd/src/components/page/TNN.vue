<template>
    <div>
        <div class="container">

            <el-container>
                <el-header>神经网络框架图</el-header>
                <div class="demo-image__preview">
                    <el-image
                        :src="tnnurl"
                        :preview-src-list="srcList"
                        :fit="fit"
                        >

                    </el-image>
                </div>
            </el-container>

            <el-divider></el-divider>

            <el-container>
                <el-row>
                    <span>设计思想介绍:</span>
                    <i class="el-icon-s-opportunity" style="padding-left: 2px"></i>
                </el-row>

                <div class="introduction">
                    <span>&emsp;&emsp;借鉴NNRF树结构的思想，把特征分组输入不同的神经网络，
                        再借鉴DLA的思想，把结果进行aggression，
                        最后由一个神经网络综合所有的结果得出最终的结果</span>
                </div>

            </el-container>

            <el-divider></el-divider>

            <el-row gutter="40">
                <el-col :span="12">
                    <el-card shadow="hover" class="mgb20" style="height:602px;">
                        <div slot="header" class="clearfix">
                            <span>训练loss图</span>
                            <i class="el-icon-s-data" style="padding-left: 20px"></i>
                        </div>


                        <div class="blocks" id="lossPicture">

                        </div>


                    </el-card>

                </el-col>

                <el-col :span="12">
                    <el-card shadow="hover" style="height:602px;">
                        <div slot="header" class="clearfix">
                            <span>拟合效果图</span>
                            <i class="el-icon-s-data" style="padding-left: 20px"></i>
                        </div>

                        <div class="blocks" id="fittingDiagram">

                        </div>

                    </el-card>


                </el-col>
            </el-row>

            <el-row gutter="40">
                <el-col :span="12">
                    <el-card shadow="hover" class="mgb20" style="height:600px;">
                        <div slot="header" class="clearfix">
                            <span>稳定段总推进力均值分析图</span>
                            <i class="el-icon-s-data" style="padding-left: 20px"></i>
                        </div>
                        <div style="height: 500px;width: 580px" id="myEchart1">

                        </div>
                    </el-card>

                </el-col>

                <el-col :span="12">
                    <el-card shadow="hover" style="height:600px;">
                        <div slot="header" class="clearfix">
                            <span>稳定段刀盘扭矩均值分析图</span>
                            <i class="el-icon-s-data" style="padding-left: 20px"></i>
                        </div>
                        <div style="height: 500px;width: 580px" id="myEchart2">

                        </div>

                    </el-card>


                </el-col>
            </el-row>

            <el-row gutter="40">
                <el-col :span="12" :offset="5">

                    <el-card shadow="hover" class="mgb20" style="height:600px;">

                        <div slot="header" class="clearfix">
                            <span>稳定段推进速度均值分析图</span>
                            <i class="el-icon-s-data" style="padding-left: 20px"></i>
                        </div>

                        <div style="height: 500px;width: 580px" id="myEchart3">

                        </div>

                    </el-card>

                </el-col>
            </el-row>

        </div>
    </div>
</template>

<script>

let lossData=[
1.956098532,
0.829456783,
0.702350605,
0.616980407,
0.559293772,
0.519050448,
0.489855536,
0.467977411,
0.451771774,
0.439779034,
0.431179961,
0.423497718,
0.417489993,
0.414367374,
0.409932363,
0.407499312,
0.404932128,
0.403691187,
0.401752826,
0.400631961,
0.400701254,
0.398333356,
0.39747853,
0.396970748,
0.396397119,
0.396436126,
0.395502325,
0.395073187,
0.394689307,
0.394116812,
0.39381235,
0.394141717,
0.393137103,
0.392736148,
0.392426031,
0.3928189,
0.392354868,
0.392540574,
0.392096548,
0.39241041,
0.391713079,
0.392132136,
0.391136582,
0.390914724,
0.391139884,
0.391531929,
0.390694525,
0.39220036,
0.39160369,
0.391236712,
0.390915488,
0.389898598,
0.390404941,
0.389980387,
0.389816593,
0.390583998,
0.389552821,
0.389953043,
0.390926662,
0.390389403,
0.389116189,
0.389086385,
0.390369039,
0.38928156,
0.388618161,
0.389549851,
0.389010537,
0.389237173,
0.389173981,
0.389378338,
0.389125006,
0.38851493,
0.38981608,
0.388823972,
0.391000785,
0.389330664,
0.389111131,
0.388847637,
0.389280735,
0.388331908,
0.388703957,
0.387730832,
0.38776959,
0.387799366,
0.388736335,
0.387928669,
0.388081517,
0.387054034,
0.38795575,
0.387510056,
0.388106519,
0.388982604,
0.389949287,
0.387803826,
0.38731268,
0.388102188,
0.387170183,
0.387002542,
0.386590776,
0.388501594,
];
let lossData1=[
0.915191049,
0.703186897,
0.607188695,
0.547233013,
0.507506965,
0.47808331,
0.457308474,
0.442619468,
0.432822769,
0.426227063,
0.41895186,
0.417456278,
0.416602701,
0.413063487,
0.414593894,
0.41597818,
0.411714943,
0.415205295,
0.411729586,
0.413676846,
0.414179242,
0.412797332,
0.413137583,
0.410837417,
0.413333098,
0.412024684,
0.408745123,
0.411275327,
0.412548776,
0.413087353,
0.412321552,
0.407814686,
0.411168637,
0.411918802,
0.409096721,
0.409628461,
0.408105589,
0.406531882,
0.407277092,
0.413200878,
0.408332926,
0.40731384,
0.41075487,
0.409913515,
0.409959766,
0.405816152,
0.416745096,
0.415099906,
0.408331043,
0.409536539,
0.410747953,
0.406233648,
0.410085732,
0.408385664,
0.409980845,
0.409678073,
0.411734529,
0.414721829,
0.406069957,
0.405810821,
0.406163302,
0.409174387,
0.409546206,
0.408883217,
0.403225942,
0.410614938,
0.403229264,
0.403636121,
0.402785082,
0.404418696,
0.402082167,
0.402525463,
0.406001732,
0.403373543,
0.401018325,
0.415688289,
0.404762855,
0.404317521,
0.405499467,
0.403300965,
0.403500435,
0.404559736,
0.40227158,
0.405786282,
0.407224821,
0.406205331,
0.4050614,
0.402823927,
0.401934787,
0.402242568,
0.401084975,
0.402786238,
0.40044131,
0.40299839,
0.403657512,
0.399793987,
0.401667966,
0.401599417,
0.408024214,
0.407746779,
];
let fitData=[
0.12308473,
0.556599,
0.49937952,
0.33965608,
-0.04151451,
0.36929032,
0.22297914,
0.028432779,
-0.31160703,
0.285696,
-0.6502081,
-0.7978784,
-0.36728105,
-0.65356845,
-0.061447747,
-1.0285256,
-0.32812786,
0.6277462,
0.83891106,
0.5682391,
0.45663172,
0.50560033,
0.6328091,
0.3536277,
0.6459618,
0.6776625,
0.44725412,
0.34510174,
0.45929933,
0.5252702,
0.33502975,
0.49125397,
-0.09064778,
-0.118871026,
-0.471514,
0.11485142,
-0.08797219,
0.16739132,
0.64980346,
-0.030053355,
0.002411627,
-0.11489112,
0.07020941,
-0.031898968,
0.17110269,
0.116121314,
-0.003764159,
-0.29383934,
0.93818873,
0.97269654,
0.32009304,
0.41313362,
0.17991816,
0.7647981,
0.5733342,
0.7269912,
0.79761064,
0.65359235,
0.3788577,
0.8074453,
0.27073026,
-0.30171633,
-1.2321758,
-1.4802923,
-1.3729873,
0.64268315,
0.5102805,
0.81923354,
0.33255047,
0.1364728,
0.6481205,
0.412603,
-0.122618176,
-0.4506023,
-1.5781333,
-0.39251566,
0.6588907,
-1.6566424,
0.055515833,
0.11340224,
-1.1980715,
-1.2328157,
-1.1609476,
-1.5625216,
-1.825707,
-1.5820739,
-1.6458981,
-1.0933955,
-1.1831392,
-1.4566326,
-0.951136,
-1.0195312,
-0.9543656,
-0.30890542,
1.2292674,
1.2557297,
1.060307,
1.2278187,
-0.013997725,
0.100921296,
];
let fitData1=[
0.69049653,
0.742161713,
0.5086637,
0.300652116,
-0.230614394,
-0.247751906,
0.381827959,
0.109309287,
-1.013630389,
0.370625357,
0.447994608,
-0.14473759,
-0.309236315,
-0.248815905,
0.018581388,
-1.576047122,
-1.168175938,
0.344913279,
0.723252253,
0.329995932,
0.349882469,
0.738976835,
-0.05367463,
0.055168249,
-0.155775202,
-0.274580837,
0.3973353,
0.40199779,
0.386116126,
0.202936085,
0.325695741,
0.557026858,
0.032534215,
0.040025066,
-0.532408392,
-0.631074228,
0.242618615,
0.87101475,
-0.970847337,
0.158273842,
-0.130759826,
-0.046074409,
0.633310704,
0.561885871,
0.807845048,
0.077420457,
-0.689133989,
-0.934463722,
1.132051954,
1.020998292,
0.51866996,
0.826968766,
0.876074896,
1.321243241,
0.805261078,
1.481619419,
1.044973346,
1.258339616,
1.392748984,
1.180766433,
0.973926305,
0.948916422,
-0.44747277,
-1.452346856,
-2.23856205,
1.317484731,
1.263875443,
1.112931691,
0.069255251,
0.445258266,
1.257245499,
0.424449323,
-0.359618976,
-0.169735964,
-0.898654515,
-0.125332944,
0.93165809,
-0.156195067,
-0.068111701,
-0.087356826,
-1.104520662,
-0.946859179,
-1.002417931,
-1.248612779,
-1.57426983,
-1.564830013,
-1.573923232,
-0.332515692,
-0.808909932,
-1.173569624,
-0.432255206,
-0.560836927,
-0.649664435,
-0.484719452,
1.635651415,
1.688272132,
1.627580847,
1.404366649,
-0.161709379,
-0.636774859,
];

/**
 * 
 */
let Xdata=[];
for(let i=1;i<=100;i++)
{
    Xdata.push(i);
}

export default {
    name: 'TNN',
    data() {
        return {
            optionLoss:{
                title: {
                    text: 'Loss图'
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
                    data: Xdata
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '原数据',
                        type: 'line',
                        stack: '总量',
                        data: lossData
                    },
                    {
                        name: '预测结果',
                        type: 'line',
                        stack: '总量',
                        data: lossData1
                    },
                ]
            },

            optionFitting:{
                title: {
                    text: '拟合图'
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
                    data: Xdata
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '原数据',
                        type: 'line',
                        stack: '总量',
                        data: fitData
                    },
                    {
                        name: '预测结果',
                        type: 'line',
                        stack: '总量',
                        data: fitData1
                    },
                ]
            },

            option1:{
                xAxis: {
                    // \xB5	&#181;	&micro;	%B5	%C2%B5

                    type: 'value',
                    name: 'U'
                },
                yAxis: {
                    //\u2202	&#8706;	&part;	%u2202

                    type: 'value',
                    name: 'O'
                },
                series: [{
                    symbolSize: 20,
                    data: [
                        [10.0, 8.04],
                        [8.0, 6.95],
                        [13.0, 7.58],
                        [9.0, 8.81],
                        [11.0, 8.33],
                        [14.0, 9.96],
                        [6.0, 7.24],
                        [4.0, 4.26],
                        [12.0, 10.84],
                        [7.0, 4.82],
                        [5.0, 5.68]
                    ],
                    type: 'scatter'
                }]
            },

            tnnurl:require('@/assets/img/模型图-tnn.png'),
            srcList: require('@/assets/img/模型图-tnn.png'),
            //     [
            //     '@/assets/img/模型图-tnn.png',
            //     // require('@/assets/img/模型图-tnn.png')
            // ],

            FittingDiagram:'https://i.postimg.cc/zDSjpbqw/Live-broadcast.jpg',
            LossDiagram:'https://i.postimg.cc/zDSjpbqw/Live-broadcast.jpg',
            fit:'scale-down',

            imgs3:require('@/assets/img/Loss1.png'),
            imgs4:require('@/assets/img/Loss2.png'),

        }
    },
    mounted() {

        let myChart1=this.$echarts.init(document.getElementById('myEchart1'));
        let myChart2=this.$echarts.init(document.getElementById('myEchart2'));
        let myChart3=this.$echarts.init(document.getElementById('myEchart3'));

        let myChartLoss=this.$echarts.init(document.getElementById('lossPicture'));
        let myChartFitting=this.$echarts.init(document.getElementById('fittingDiagram'));

        myChart1.setOption(this.option1);
        myChart2.setOption(this.option1);
        myChart3.setOption(this.option1);

        myChartLoss.setOption(this.optionLoss);
        myChartFitting.setOption(this.optionFitting);

    },
    methods(){

    }

};

</script>

<style scoped>


.el-image__inner{
    width: 100px;
    height: 100px;

    display: inline-block;
}

.el-image img{
    width: auto;
    height: auto;
    max-width: 100%;
    max-height: 100%;
    display: block;
}


.blocks{
    height: 400px;
}

.demo-image__preview{
    /*display: grid;*/
    position: relative;
    padding-left: 250px;
    padding-top: 30px;
}

.el-header{
    background-color: #B3C0D1;
    font-size: 20px;
    line-height: 60px;
    align-content: center;
    font-weight: bolder;
    text-align: center;
}

.el-upload__text{
    width: 100px;
    height: 100px;
}

.el-card{
    background: #c7ddef;
}

.clearfix{
    font-weight: bolder;
}

.user-info {
    display: flex;
    align-items: center;

    border-bottom: 2px solid #ccc;

    font-weight:bolder;
}


.user-info-list {
    font-size: 14px;
    color: #999;
    line-height: 25px;
}

.user-info-list span {
    margin-left: 70px;
}

.mgb20 {
    margin-bottom: 20px;
}




</style>