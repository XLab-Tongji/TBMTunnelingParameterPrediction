<template>

    <div class="container">

        <div id="contrast" class="frameContrast">
                <div class="h1title">比对模型</div>
                <div style="margin-left: 30px">

                    <el-card shadow="hover" class="mgb20" >
                        <div class="block" >
                        <div style="float: left;width: 250px;height: 250px;margin-right: 30px">
                            <el-image
                                style="width: 250px; height: 250px; border-radius: 50%;"
                                :src="imgs2"
                                :preview-src-list="imgs2"
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
                                style="width: 250px; height: 250px; border-radius: 50%;"
                                :src="imgs1"
                                :preview-src-list="imgs1"
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
                <div style="width: 800px;padding-left: 40px;padding-top: 20px">
                    <el-table :data="TableData" stripe style="width: 100%" border>
                        <el-table-column prop="a" label="上升段撑靴压力均值">
                        </el-table-column>
                        <el-table-column prop="b" label="上升段撑靴压力方差">
                        </el-table-column>
                        <el-table-column prop="c" label="上升段刀盘转速均值">
                        </el-table-column>
                        <el-table-column prop="d" label="上升段刀盘转速方差">
                        </el-table-column>
                        <el-table-column prop="e" label="上升段刀盘刹车压力均值">
                        </el-table-column>
                        <el-table-column prop="f" label="上升段刀盘刹车压力方差">
                        </el-table-column>
                        <el-table-column prop="g" label="上升段刀盘扭矩均值">
                        </el-table-column>
                        <el-table-column prop="h" label="上升段刀盘扭矩方差">
                        </el-table-column>
                        <el-table-column prop="i" label="上升段刀盘功率均值">
                        </el-table-column>
                        <el-table-column prop="j" label="上升段刀盘功率方差">
                        </el-table-column>
                        <el-table-column prop="k" label="上升段推进压力均值">
                        </el-table-column>
                        <el-table-column prop="l" label="上升段推进压力方差">
                        </el-table-column>
                        <el-table-column prop="m" label="上升段贯入度均值">
                        </el-table-column>
                        <el-table-column prop="n" label="上升段贯入度方差">
                        </el-table-column>
                        <el-table-column prop="o" label="上升段总推进力均值">
                        </el-table-column>
                        <el-table-column prop="p" label="上升段总推进力方差">
                        </el-table-column>
                        <el-table-column prop="q" label="上升段推进速度均值">
                        </el-table-column>
                        <el-table-column prop="r" label="上升段推进速度方差">
                        </el-table-column>
                        <el-table-column prop="s" label="上升段推进位移均值">
                        </el-table-column>
                        <el-table-column prop="t" label="上升段推进位移方差">
                        </el-table-column>
                        <el-table-column prop="u" label="上升段主机皮带机转速均值">
                        </el-table-column>
                        <el-table-column prop="v" label="上升段主机皮带机转速方差">
                        </el-table-column>
                        <el-table-column prop="w" label="上升段桥架皮带机转速均值">
                        </el-table-column>
                        <el-table-column prop="x" label="上升段桥架皮带机转速方差">
                        </el-table-column>
                        <el-table-column prop="y" label="上升段转渣皮带机转速均值">
                        </el-table-column>
                        <el-table-column prop="z" label="上升段转渣皮带机转速方差">
                        </el-table-column>
                        <el-table-column prop="aa" label="稳定段总推进力均值">
                        </el-table-column>
                        <el-table-column prop="ab" label="稳定段刀盘扭矩均值">
                        </el-table-column>
                        <el-table-column prop="ac" label="稳定段推进速度均值">
                        </el-table-column>
                    </el-table>
                </div>
                <div style="width: 800px;height: 80px;padding-left: 620px;padding-top: 30px">
                    <el-button type="primary" icon="el-icon-refresh" @click="NewSample">换一批</el-button>
                    <el-button type="primary" @click="TestResult">测试<i class="el-icon-orange el-icon--right"></i></el-button>
                </div>
            </div>

        <div id="testResult" class="frameContrast">
                <div class="h1title">测试结果</div>
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

<!--                <el-popover v-for="item in catalogs"-->
<!--                            placement="top-start"-->
<!--                            width="200"-->
<!--                            trigger="hover"-->
<!--                            style="padding: 25px">-->
<!--                    <div v-for="opt in item[1]"  class="text item">-->
<!--                        {{ opt }}-->
<!--                    </div>-->
<!--                    <el-tag slot="reference" style="background-color: white;color:#ff5555;border:1px solid">{{item[0]}}</el-tag>-->
<!--                </el-popover>-->



            </div>


<!--        <div class="frameContrast">-->
<!--            <div style="margin-top: 20px">-->

<!--                <el-table-->
<!--                    :data="tables"-->
<!--                    ref="multipleTable"-->
<!--                    tooltip-effect="dark"-->
<!--                    style="width: 100%"-->
<!--                    @selection-change='selectArInfo'>-->

<!--                    <el-table-column type="selection" width="45px"></el-table-column>-->
<!--                    <el-table-column label="序号" width="62px" type="index">-->
<!--                    </el-table-column>-->
<!--                    <template v-for='(col) in tableData'>-->
<!--                        <el-table-column-->
<!--                            sortable-->
<!--                            :show-overflow-tooltip="true"-->
<!--                            :prop="col.dataItem"-->
<!--                            :label="col.dataName"-->
<!--                            :key="col.dataItem"-->
<!--                            width="124px">-->
<!--                        </el-table-column>-->
<!--                    </template>-->
<!--                    <el-table-column label="操作" width="80" align="center">-->
<!--                        <template slot-scope="scope">-->
<!--                            <el-button size="mini" class="del-com" @click="delTabColOne()" ><i class="iconfont icon-shanchu"></i></el-button>-->
<!--                        </template>-->
<!--                    </el-table-column>-->
<!--                </el-table>-->


<!--            </div>-->
<!--        </div>-->

    </div>
</template>


<script>
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min";


export default {
    baseURL:'http://localhost:8080',
    name: 'FrameworkDesign',

    data() {
        return {

            TableData: [
                {
                    a:"1",
                    b:"2",
                    c:"3",
                    d:"4",
                    e:"5",
                    f:"6",
                    g:"7",
                    h:"8",
                    i:"9",
                    j:"10",
                    k:"11",
                    l:"12",
                    m:"13",
                    n:"14",
                    o:"15",
                    p:"16",
                    q:"17",
                    r:"18",
                    s:"19",
                    t:"20",
                    u:"21",
                    v:"22",
                    w:"23",
                    x:"24",
                    y:"25",
                    z:"26",
                    aa:"27",
                    ab:"28",
                    ac:"29",
                },
                {
                    a:"1",
                    b:"2",
                    c:"3",
                    d:"4",
                    e:"5",
                    f:"6",
                    g:"7",
                    h:"8",
                    i:"9",
                    j:"10",
                    k:"11",
                    l:"12",
                    m:"13",
                    n:"14",
                    o:"15",
                    p:"16",
                    q:"17",
                    r:"18",
                    s:"19",
                    t:"20",
                    u:"21",
                    v:"22",
                    w:"23",
                    x:"24",
                    y:"25",
                    z:"26",
                    aa:"27",
                    ab:"28",
                    ac:"29",
                },
                {
                    a:"1",
                    b:"2",
                    c:"3",
                    d:"4",
                    e:"5",
                    f:"6",
                    g:"7",
                    h:"8",
                    i:"9",
                    j:"10",
                    k:"11",
                    l:"12",
                    m:"13",
                    n:"14",
                    o:"15",
                    p:"16",
                    q:"17",
                    r:"18",
                    s:"19",
                    t:"20",
                    u:"21",
                    v:"22",
                    w:"23",
                    x:"24",
                    y:"25",
                    z:"26",
                    aa:"27",
                    ab:"28",
                    ac:"29",
                },
                {
                    a:"1",
                    b:"2",
                    c:"3",
                    d:"4",
                    e:"5",
                    f:"6",
                    g:"7",
                    h:"8",
                    i:"9",
                    j:"10",
                    k:"11",
                    l:"12",
                    m:"13",
                    n:"14",
                    o:"15",
                    p:"16",
                    q:"17",
                    r:"18",
                    s:"19",
                    t:"20",
                    u:"21",
                    v:"22",
                    w:"23",
                    x:"24",
                    y:"25",
                    z:"26",
                    aa:"27",
                    ab:"28",
                    ac:"29",
                },
                {
                    a:"1",
                    b:"2",
                    c:"3",
                    d:"4",
                    e:"5",
                    f:"6",
                    g:"7",
                    h:"8",
                    i:"9",
                    j:"10",
                    k:"11",
                    l:"12",
                    m:"13",
                    n:"14",
                    o:"15",
                    p:"16",
                    q:"17",
                    r:"18",
                    s:"19",
                    t:"20",
                    u:"21",
                    v:"22",
                    w:"23",
                    x:"24",
                    y:"25",
                    z:"26",
                    aa:"27",
                    ab:"28",
                    ac:"29",
                },
                {
                    a:"1",
                    b:"2",
                    c:"3",
                    d:"4",
                    e:"5",
                    f:"6",
                    g:"7",
                    h:"8",
                    i:"9",
                    j:"10",
                    k:"11",
                    l:"12",
                    m:"13",
                    n:"14",
                    o:"15",
                    p:"16",
                    q:"17",
                    r:"18",
                    s:"19",
                    t:"20",
                    u:"21",
                    v:"22",
                    w:"23",
                    x:"24",
                    y:"25",
                    z:"26",
                    aa:"27",
                    ab:"28",
                    ac:"29",
                },
                {
                    a:"1",
                    b:"2",
                    c:"3",
                    d:"4",
                    e:"5",
                    f:"6",
                    g:"7",
                    h:"8",
                    i:"9",
                    j:"10",
                    k:"11",
                    l:"12",
                    m:"13",
                    n:"14",
                    o:"15",
                    p:"16",
                    q:"17",
                    r:"18",
                    s:"19",
                    t:"20",
                    u:"21",
                    v:"22",
                    w:"23",
                    x:"24",
                    y:"25",
                    z:"26",
                    aa:"27",
                    ab:"28",
                    ac:"29",
                },
                {
                    a:"1",
                    b:"2",
                    c:"3",
                    d:"4",
                    e:"5",
                    f:"6",
                    g:"7",
                    h:"8",
                    i:"9",
                    j:"10",
                    k:"11",
                    l:"12",
                    m:"13",
                    n:"14",
                    o:"15",
                    p:"16",
                    q:"17",
                    r:"18",
                    s:"19",
                    t:"20",
                    u:"21",
                    v:"22",
                    w:"23",
                    x:"24",
                    y:"25",
                    z:"26",
                    aa:"27",
                    ab:"28",
                    ac:"29",
                },
                {
                    a:"1",
                    b:"2",
                    c:"3",
                    d:"4",
                    e:"5",
                    f:"6",
                    g:"7",
                    h:"8",
                    i:"9",
                    j:"10",
                    k:"11",
                    l:"12",
                    m:"13",
                    n:"14",
                    o:"15",
                    p:"16",
                    q:"17",
                    r:"18",
                    s:"19",
                    t:"20",
                    u:"21",
                    v:"22",
                    w:"23",
                    x:"24",
                    y:"25",
                    z:"26",
                    aa:"27",
                    ab:"28",
                    ac:"29",
                },
                {
                    a:"1",
                    b:"2",
                    c:"3",
                    d:"4",
                    e:"5",
                    f:"6",
                    g:"7",
                    h:"8",
                    i:"9",
                    j:"10",
                    k:"11",
                    l:"12",
                    m:"13",
                    n:"14",
                    o:"15",
                    p:"16",
                    q:"17",
                    r:"18",
                    s:"19",
                    t:"20",
                    u:"21",
                    v:"22",
                    w:"23",
                    x:"24",
                    y:"25",
                    z:"26",
                    aa:"27",
                    ab:"28",
                    ac:"29",
                }
            ],
            Result:[
                {
                    R2:"0",
                    RMSE:"0",
                    MAE:"0"
                },
                {
                    R2:"0",
                    RMSE:"0",
                    MAE:"0"
                }
            ],

            imgs1:[require("@/assets/img/Tan2.png")],
            imgs2:[require("@/assets/img/Tan3.png")],


            tables: [
                {
                xiaoxue: '福兰',
                chuzhong: '加芳',
                gaozhong: '蒲庙',
                daxue: '西安',
                yanjiusheng: '西安',
                shangban: '北京'
            }, {
                xiaoxue: '南坊',
                chuzhong: '礼泉',
                gaozhong: '礼泉',
                daxue: '西安',
                yanjiusheng: '西安',
                shangban: '南坊'
            }, {
                xiaoxue: '马山',
                chuzhong: '加芳',
                gaozhong: '蒲庙',
                daxue: '西安',
                yanjiusheng: '重庆',
                shangban: '北京'
            }],
            tableData: [
                {
                dataItem: 'xiaoxue',
                dataName: '小学'
            }, {
                dataItem: 'chuzhong',
                dataName: '初中'
            }, {
                dataItem: 'gaozhong',
                dataName: '高中'
            }, {
                dataItem: 'daxue',
                dataName: '大学'
            }, {
                dataItem: 'yanjiusheng',
                dataName: '研究生'
            }, {
                dataItem: 'shangban',
                dataName: '上班'
            }]

            // catalogs:[
            //     [
            //         '闲置数码',
            //         [
            //             '手机','iphone','text'
            //         ]
            //     ],
            //     [
            //         '家居日用',
            //         ['电风扇','拖把']
            //     ],
            //     [
            //         '鞋服配饰',
            //         ['女装','男装','童装','配饰']
            //     ],
            //     [
            //         '书本文具',
            //         ['文学','科技']
            //     ],
            //     [
            //         '食品零食',
            //         ['饮品','零食']
            //     ],
            //     [
            //         '线下交易',
            //         ['同城','异地']
            //     ]
            // ]
        }
    },
    mounted() {
        this.NewSample();
    },
    methods:{
        NewSample(){
            this.http.get(this.publicPath+'api/取得十个样例')
            .then(function(res){
                let array=res.list();
                let i=0;
                array.forEach(function(item){
                    this.tableData[i].a=item.a;
                    this.tableData[i].b=item.b;
                    this.tableData[i].c=item.c;
                    this.tableData[i].d=item.d;
                    this.tableData[i].e=item.e;
                    this.tableData[i].f=item.f;
                    this.tableData[i].g=item.g;
                    this.tableData[i].h=item.h;
                    this.tableData[i].i=item.i;
                    this.tableData[i].j=item.j;
                    this.tableData[i].k=item.k;
                    this.tableData[i].l=item.l;
                    this.tableData[i].m=item.m;
                    this.tableData[i].n=item.n;
                    this.tableData[i].o=item.o;
                    this.tableData[i].p=item.p;
                    this.tableData[i].q=item.q;
                    this.tableData[i].r=item.r;
                    this.tableData[i].s=item.s;
                    this.tableData[i].t=item.t;
                    this.tableData[i].u=item.u;
                    this.tableData[i].v=item.v;
                    this.tableData[i].w=item.w;
                    this.tableData[i].x=item.x;
                    this.tableData[i].y=item.y;
                    this.tableData[i].z=item.z;
                    this.tableData[i].aa=item.aa;
                    this.tableData[i].ab=item.ab;
                    this.tableData[i].ac=item.ac;
                    i++;
                })
            })
            .catch()
            {
                console.error("后端获取样例失败")
            }
        },
        TestResult(){
            this.http.get(this.baseURL+'api/模型测试数据')
            .then(function(res){
                this.Result[0].R2=res.R2;
                this.Result[0].RMSE=res.RMSE,
                this.MAE=res.MAE
            })
            .catch()
            {
                console.error("后端获取结果数据失败")
            }

        }
    }

};


</script>

<style scoped>

.frameContrast{
    width: 1100px;
    padding-top: 10px;
    margin-bottom: 10px;
}

#contrast{
    background: #1b6d85;
    height: 850px;
}


.h1title{
    font-weight: bolder;
    margin-left: 20px;
    font-size: 30px;
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
    color: #dd6161;
    background: #97a8be;
    margin-top: 20px;
}


#testData{
    background: #8c939d;

}

#testResult{
    background: #c7ddef;
    height: 700px;
}


</style>