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

            <div style="float: left;width: 30px"></div>
            <div class="h1title" style="float: left;margin-bottom: 20px">测试数据</div>

            <div style="width: 1000px;padding-left: 40px;padding-top: 20px;margin-top:100px;background:#c7ddef">
                <el-table
                    :data="TableData"
                    stripe
                    style="width: 100%"
                    border
                >
                    <el-table-column
                        v-for="info in TestHeader" :key="info.key"
                        :property="info.key"
                        :label="info.label"
                    >
                        <template slot-scope="scope">
                            {{scope.row[scope.column.property]}}
                        </template>
                    </el-table-column>
                </el-table>
            </div>

            <div style="width: 800px;height: 80px;padding-left: 620px;padding-top: 30px;background:#c7ddef">
                <el-button type="primary" icon="el-icon-refresh" @click="NewSample">换一批</el-button>
                <el-button type="primary" @click="TestResult">测试<i class="el-icon-orange el-icon--right"></i></el-button>
            </div>

        </div>

        <div id="testResult" class="frameContrast">
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
            <!--                <el-popover v-for="(item,index) in catalogs"-->
            <!--                            placement="top-start"-->
            <!--                            width="200"-->
            <!--                            trigger="hover"-->
            <!--                            style="padding: 25px"-->
            <!--                            :key="index">-->
            <!--                    <div v-for="opt in item[1]"  class="text item">-->
            <!--                        {{ opt }}-->
            <!--                    </div>-->
            <!--                    <el-tag slot="reference" style="background-color: white;color:#ff5555;border:1px solid">{{item[0]}}</el-tag>-->
            <!--                </el-popover>-->
        </div>

    </div>
</template>


<script>
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min";


export default {
    baseURL:'http://localhost:8080',
    name: 'FrameworkDesign1',

    data() {
        return {
            fit:'scale-down',

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

            TestHeader:[
                { key:"a" ,label:"上升段撑靴压力均值"},

                { key:"b" ,label:"上升段撑靴压力方差"},

                { key:"c" ,label:"上升段刀盘转速均值"},

                { key:"d" ,label:"上升段刀盘转速方差"},

                { key:"e" ,label:"上升段刀盘刹车压力均值"},

                { key:"f" ,label:"上升段刀盘刹车压力方差"},

                { key:"g" ,label:"上升段刀盘扭矩均值"},

                { key:"h" ,label:"上升段刀盘扭矩方差"},

                { key:"i" ,label:"上升段刀盘功率均值"},

                { key:"j" ,label:"上升段刀盘功率方差"},

                { key:"k" ,label:"上升段推进压力均值"},

                { key:"l" ,label:"上升段推进压力方差"},

                { key:"m" ,label:"上升段贯入度均值"},

                { key:"n" ,label:"上升段贯入度方差"},

                { key:"o" ,label:"上升段总推进力均值"},

                { key:"p" ,label:"上升段总推进力方差"},

                { key:"q" ,label:"上升段推进速度均值"},

                { key:"r" ,label:"上升段推进速度方差"},

                { key:"s" ,label:"上升段推进位移均值"},

                { key:"t" ,label:"上升段推进位移方差"},

                { key:"u" ,label:"上升段主机皮带机转速均值"},

                { key:"v" ,label:"上升段主机皮带机转速方差"},

                { key:"w" ,label:"上升段桥架皮带机转速均值"},

                { key:"x" ,label:"上升段桥架皮带机转速方差"},

                { key:"y" ,label:"上升段转渣皮带机转速均值"},

                { key:"z",label:"上升段转渣皮带机转速方差"},

                { key:"aa" ,label:"稳定段总推进力均值"},

                { key:"ab", label:"稳定段刀盘扭矩均值"},

                { key:"ac",label:"稳定段推进速度均值"}



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


            rightHeader: [
                {
                    label: '编码',
                    key: 'code'
                },
                {
                    label: '姓名',
                    key: 'name'
                },
                {
                    label: '权限描述',
                    key: 'description'
                }
            ],
            rightsDate:[
                {
                    "id":221,
                    "code": "01",
                    "name": "西药开立权限",
                    "description": "医生对西药处方权限",
                    "ifUse":"0"
                },
                {
                    "id":222,
                    "code": "02",
                    "name": "草药开立权限",
                    "description": "医生对草药处方权限",
                    "ifUse":"0"
                },
                {
                    "id":223,
                    "code": "03",
                    "name": "成药开立权限",
                    "description": "医生对成药处方权限",
                    "ifUse":"0"
                },
                {
                    "id":224,
                    "code": "04",
                    "name": "麻醉开立权限",
                    "description": "医生对麻醉处方权限",
                    "ifUse":"0"
                },
                {
                    "id":225,
                    "code": "05",
                    "name": "精一开立权限",
                    "description": "医生对精一处方权限",
                    "ifUse":"0"
                }
            ],
        }
    },
    mounted() {
        this.NewSample();
    },
    methods:{
        NewSample(){
            this.$http.get(this.publicPath+'api/取得十个样例')
                .then(function(res){
                    let array=res.data;

                    let i=0;
                    array.forEach(function(item){

                        this.TableData[i].a=item.a;
                        this.TableData[i].b=item.b;
                        this.TableData[i].c=item.c;
                        this.TableData[i].d=item.d;
                        this.TableData[i].e=item.e;
                        this.TableData[i].f=item.f;
                        this.TableData[i].g=item.g;
                        this.TableData[i].h=item.h;
                        this.TableData[i].i=item.i;
                        this.TableData[i].j=item.j;
                        this.TableData[i].k=item.k;
                        this.TableData[i].l=item.l;
                        this.TableData[i].m=item.m;
                        this.TableData[i].n=item.n;
                        this.TableData[i].o=item.o;
                        this.TableData[i].p=item.p;
                        this.TableData[i].q=item.q;
                        this.TableData[i].r=item.r;
                        this.TableData[i].s=item.s;
                        this.TableData[i].t=item.t;
                        this.TableData[i].u=item.u;
                        this.TableData[i].v=item.v;
                        this.TableData[i].w=item.w;
                        this.TableData[i].x=item.x;
                        this.TableData[i].y=item.y;
                        this.TableData[i].z=item.z;
                        this.TableData[i].aa=item.aa;
                        this.TableData[i].ab=item.ab;
                        this.TableData[i].ac=item.ac;
                        i++;
                    })
                })
                .catch()
            {
                console.error("后端获取样例失败")
            }
        },
        TestResult(){
            this.$http.get(this.baseURL+'api/模型测试数据')
                .then(function(res){
                    this.Result[0].R2=res.R2;
                    this.Result[0].RMSE=res.RMSE;
                    this.MAE=res.MAE;
                })
                .catch()
            {
                console.error("后端获取结果数据失败")
            }

        },
    }
};


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
    height: 700px;
}


</style>