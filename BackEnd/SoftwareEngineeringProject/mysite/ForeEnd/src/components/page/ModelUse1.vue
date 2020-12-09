<template>
    <div>
        <div class="container">
            <div style="height: 600px;">
                <el-steps direction="vertical" :active=number id="mainStep">

                    <el-step title="文件上传">
                        <template slot="description">

                            <el-upload
                                class="upload-demo"
                                accept=".zip"
                                action="uploadZip"
                                ref="refFile"

                                :auto-upload="false"
                                :on-change="uploadZip"
                                :on-preview="handlePreview"
                                :on-remove="handleRemove"
                                :before-remove="beforeRemove"
                                :before-upload="beforeAvatarUpload"
                                :on-exceed="handleExceed"
                                :limit="1"
                                :file-list="fileList">
                                <el-button size="small" type="primary"
                                >文件上传</el-button>
                                <el-button style="margin-left: 10px;" size="small" type="success" @click="uploadZip">上传到服务器</el-button>
                                <div slot="tip" class="el-upload__tip">只能上传zip文件，且不超过500kb {{message}}</div>
                            </el-upload>


                        </template>
                    </el-step>

                    <el-step title="数据预处理">
                        <template slot="description">

                            <div class="ellipse">
                                <div class="models">数据预处理</div>
                            </div>
                        </template>
                    </el-step>

                    <el-step title="模型调用和预测" description="这是一段很长很长很长的描述性文字">
                        <template slot="description">
                            <div class="ellipse">
                                <div class="models">模型调用和预测</div>
                            </div>
                        </template>
                    </el-step>

                </el-steps>
            </div>

            <br>
            <el-row style="margin-top: 200px">
                <el-col :span="23">
                    <el-card shadow="hover" class="mgb20" style="height:252px;">
                        <div class="user-info">
                            特征数据提取结果
                        </div>
                        <div class="user-info-list">
                            <span>数据为空</span>
                        </div>

                    </el-card>
                    <el-card shadow="hover" style="height:252px;">
                        <div slot="header" class="clearfix">
                            <span>模型预测结果</span>
                        </div>
                        <span>数据为空</span>
                    </el-card>
                </el-col>
            </el-row>


        </div>






    </div>
</template>

<script>
export default {

    name: "ModelUse1",
    baseURL:'http://localhost:8080',
    data() {
        return {
            name: localStorage.getItem('ms_username'),
            fileList: [
                // {
                //     name:'Amonkey0.7z',
                //     url:'d:/Amonkey0.7z'
                // }
            ],

            TNNData:[
                //         时间戳	运行时间	桩号	前点偏差X	前点偏差Y	前盾俯仰角	前盾滚动角	主液压油箱温度	液压油箱温度预警设置	液压油箱温度报警设置	温度误差设置	左侧护盾压力	右侧护盾压力	顶护盾压力	左侧楔形油缸压力	右侧楔形油缸压力	左侧扭矩油缸伸出压力	左侧扭矩油缸回收压力	右侧扭矩油缸伸出压力	右侧扭矩油缸回收压力	左侧后支撑压力	右侧后支撑压力	撑靴压力	左侧护盾位移	右侧护盾位移	左侧扭矩油缸位移	右侧扭矩油缸位移	内循环水罐温度	内循环水罐液位	冷水箱温度	冷水箱液位	热水箱温度	热水箱液位	刀盘喷水压力	刀盘喷水增压泵压力	污水箱压力检测	TBM外水进水温度	TBM主冷却器进水温度	暖水泵压力	冷水泵压力	内水泵压力	变频器1温度	变频器2温度	暖水箱自动排水温度设置	二次风机频率设置	齿轮油温度	EP2泵 出口压力检测	EP2 内密封压力	EP2 外密封压力	齿轮润滑油箱压力液位1	齿轮润滑油箱压力液位2	泵1润滑压力	泵2润滑压力	泵3润滑压力	泵4润滑压力	齿轮密封压力	齿轮回油泵出口压力	主驱动加压压力	润滑泵电机电流	外密封腔流量	外密封流量	齿轮润滑流量1	齿轮润滑流量2	前部小齿轮轴承润滑流量1	前部小齿轮轴承润滑流量2	后部小齿轮轴承润滑流量1	后部小齿轮轴承润滑流量2	齿轮密封外密封压力	齿轮密封内密封压力	齿轮油温度预警设置	齿轮油温度报警设置	EP2次数设置	主驱动1#电机电流	主驱动2#电机电流	主驱动3#电机电流	主驱动4#电机电流	主驱动5#电机电流	主驱动6#电机电流	主驱动7#电机电流	主驱动8#电机电流	主驱动9#电机电流	主驱动10#电机电流	主驱动1#电机扭矩	主驱动2#电机扭矩	主驱动3#电机扭矩	主驱动4#电机扭矩	主驱动5#电机扭矩	主驱动6#电机扭矩	主驱动7#电机扭矩	主驱动8#电机扭矩	主驱动9#电机扭矩	主驱动10#电机扭矩	主驱动1#电机输出频率	主驱动2#电机输出频率	主驱动3#电机输出频率	主驱动4#电机输出频率	主驱动5#电机输出频率	主驱动6#电机输出频率	主驱动7#电机输出频率	主驱动8#电机输出频率	主驱动9#电机输出频率	主驱动10#电机输出频率	主驱动1#电机输出功率	主驱动2#电机输出功率	主驱动3#电机输出功率	主驱动4#电机输出功率	主驱动5#电机输出功率	主驱动6#电机输出功率	主驱动7#电机输出功率	主驱动8#电机输出功率	主驱动9#电机输出功率	主驱动10#电机输出功率	减速机1#温度	减速机2#温度	减速机3#温度	减速机4#温度	减速机5#温度	减速机6#温度	减速机7#温度	减速机8#温度	减速机9#温度	减速机10#温度	刀盘转速	刀盘转速电位器设定值	刀盘刹车压力	刀盘扭矩	刀盘给定转速显示值	刀盘速度给定	刀盘功率	刀盘运行时间	刀盘运行时间.1	给定频率	变频柜回水温度报警值	变频柜回水温度停机值	减速机温度报警值	减速机温度停机值	刀盘最低转速设置	左撑靴小腔压力	右撑靴小腔压力	推进压力	贯入度	总推进力	推进速度	推进位移	推进泵电机电流	撑靴泵电机电流	换步泵电机电流	左推进油缸行程检测	右推进油缸行程检测	左撑靴油缸行程检测	右撑靴油缸行程检测	推进速度电位器设定值	推进泵压力	控制油路2压力检测	辅助系统压力检测	推进速度给定百分比	左撑靴俯仰角	左撑靴滚动角	右撑靴俯仰角	右撑靴滚动角	控制泵压力	控制油路1 压力	换步泵1 压力	撑靴泵压力	换步泵2 压力	钢拱架泵压力	主机皮带机泵压力	左倾最大滚动角设置	右倾最大滚动角设置	左撑靴最大滚动角设置	左撑靴最大俯仰角设置	右撑靴最大滚动角设置	右撑靴最大俯仰角设置	撑靴压力设定	推进位移最大允许偏差设置	贯入度设置	推进给定速度百分比	推进速度.1	刀盘CH4气体浓度	刀盘H2S浓度	控制室O2浓度	控制室CO浓度	控制室CO2浓度	设备桥CH4浓度	拖车尾部CH4浓度	左拖拉油缸压力	右拖拉油缸压力	拖拉油缸最大允许压力设置	拖拉油缸最小允许压力设置	机械手泵1 电机电流	机械手泵2 电机电流	主机皮带机转速	桥架皮带机转速	转渣皮带机转速	主机皮带机泵电机电流	主皮带机转速电位器设定值	桥架皮带机转速电位器设定值	转渣皮带机转速电位器设定值
                //         1.5105E+12	2017/11/13 0:12	53207.41797	-28.0352993	-19.16120148	0.664000094	-0.019998569	47.26200867	50	65	2	34.38946915	18.34490776	58.95543671	67.43344879	63.29571533	47.81539536	9.432869911	49.42129517	0.115740739	16.95601845	23.4375	295.5295105	160.8217621	160.5305939	-2.111541748	-5.041893005	29.82494164	0	28.30222893	1695.755615	31.53211784	1782.761841	6.829861164	8.902777672	-999	4.213686466	22.77560806	7.298611164	5.02314806	4.954282284	29.98770142	26.63122177	45	50	32.06741714	180.8738403	-999	0.041666668	742.6269531	1098.546021	28.61689758	35.55410767	23.32176018	27.74884415	4.568142414	0.105324075	0	28.30138588	5.759999752	96	7.979167461	12.13020897	10.58854198	9.010416985	13.46614647	9.015625	0	0	50	60	110	181.3000031	182.1999969	0	183.8999939	192.1999969	184.8000031	167.8000031	0	183.5	180.3999939	-6.732000351	26.9280014	0	6.732000351	0	-16.82999992	6.732000351	0	23.56200027	-3.366000175	0.200000003	0.100000001	0	0.100000001	0.200000003	0.100000001	0.200000003	0	0.100000001	0.100000001	0	0	0	0	0	0	0	0	0	0	-999	-999	-999	-999	-999	-999	-999	-999	-999	-999	0.010917501	0	44.32725525	9.261161804	0	0	0	5609	13	0	45	55	65	80	1	-9999	12.58680534	1.302083254	0	0	0	25.88903809	54.32183075	37.90798569	0.496527791	-0.102294922	1.509124756	431.798645	394.7927856	2658.05835	22.51157379	113.7152786	209.6932831	0	2.389323235	-0.894458771	1.053240776	0.4618783	127.0688629	24.18981552	0.318287045	302.4305725	0.405092597	190.5381927	88.84548187	5	5	5	5	5	5	320	29	15	26.58058357	0	-999	0	25	0	0.002712674	2.09780097	-999	57.40740967	1.056134224	250	0	45.52539063	0	1.975250721	2.678216457	2.69090867	63.078125	2.967013836	3	2.924262047
                // 1.5105E+12	2017/11/13 0:12	53207.41797	-28.0352993	-19.16120148	0.664000094	-0.019998569	47.36689758	50	65	2	34.40393448	18.33044052	58.95543671	67.37557983	63.31018829	47.82986069	9.375	49.37789536	0.101273149	16.95601845	23.45196724	295.4571838	160.7964478	160.5179443	-2.111541748	-5.066467285	29.82855988	0	28.29499626	1696.021118	31.53935051	1790.458618	8.710069656	8.831018448	-999	4.217303276	22.7792244	7.305555344	5.04745388	4.949652672	29.98770142	26.63122177	45	50	32.07103729	180.8738403	-999	0.038773149	743.8584595	1095.261841	28.54166794	35.52517319	23.2421875	27.74884415	4.58622694	0.103009261	0	28.29652596	11.5199995	96	8.038194656	12.13802052	13.28125095	9.032986641	13.70572853	9.149306297	0	0	50	60	110	139.3999939	143.3999939	0	145.5	136.8000031	111.5999985	121.5999985	0	132	132.5	26.9280014	117.8099976	0	100.9799957	-6.732000351	6.732000351	94.2480011	0	100.9799957	67.31999969	0.300000012	0.300000012	0	0.300000012	0.300000012	0.300000012	0.300000012	0	0.300000012	0.300000012	0	0	0	0	0	0	0	0	0	0	-999	-999	-999	-999	-999	-999	-999	-999	-999	-999	0.02382	0	44.296875	127.1304932	0	0	0	5609	13	0	45	55	65	80	1	-9999	12.52893543	1.302083254	0	0	0	25.88903809	54.32183075	37.90798569	0.496527791	-0.102294922	1.509124756	431.8601074	394.7927856	2657.697021	22.39583206	113.8165436	209.2303314	0	2.38606739	-0.884331703	1.059751034	0.458260536	127.1412048	24.20428276	0.231481478	302.5607605	0.434027791	190.4947815	89.58332825	5	5	5	5	5	5	320	29	15	26.57697105	0	-999	0	25	0	0.002712674	2.517361164	-999	57.39293671	1.041666746	250	0	45.52539063	0	1.973432779	2.677534819	2.681065559	63.078125	2.966905355	3	2.924370766
            ],

            message:"",
            number:1
        };
    },
    computed: {

    },
    methods: {

        handleRemove(file, fileList) {
            console.log(file, fileList);
        },
        handlePreview(file) {
            console.log(file);
        },
        handleExceed(files, fileList) {
            this.$message.warning(`当前限制选择 1 个文件，
            本次选择了 ${files.length} 个文件，
            共选择了 ${files.length + fileList.length} 个文件`);
        },
        beforeRemove(file, fileList) {
            return this.$confirm(`确定移除 ${ file.name }？`);
        },

        beforeAvatarUpload(file){
            var FileExt = file.name.replace(/.+\./, "");
            if (['zip', 'rar','gz',".apk"].indexOf(FileExt.toLowerCase()) === -1){
                this.message="文件格式有误，请重新上传"
                return false;
            }
            this.message="上传中,请稍等"
        },

        uploadZip(file)
        {
            this.number++;
            const selectedFile = this.$refs.refFile;
            var name = selectedFile.name; //选中文件的文件名
            var size = selectedFile.size; //选中文件的大小
            console.log("文件名:" + name + "大小:" + size);



            this.http.post(this.publicPath+'api/上传zip文件包',{file})
                .then(function(response) {
                    this.$refs.refFile.clearFiles();
                    this.featureDataResult();
                })
                .catch(function(response){
                    console.log(response);
                })
        },



        featureDataResult()
        {
            this.get(this.base+'api/获取特征数据')
                .then(function(file) {
                    this.number++;
                    this.modelPredictionResults();
                })
                .catch(function(res) {
                    console.log(res);
                })
        },

        modelPredictionResults()
        {
            this.get(this.base+'api/获取模型预测结果')
                .then(function(file) {

                })
                .catch(function(res) {
                    console.log(res);
                })
        }



    }
}
</script>

<style scoped>


.upload-demo{

}


.ellipse{
    width: 250px;
    height: 150px;
    margin: 50px;
    background: #5daf34;
    border-radius: 50% / 50%;
    display: flex;
    align-items: center;        /*竖直居中 垂直居中*/
    justify-content: center;    /*水平居中*/

}

.models{
    font-weight: bolder;
    color: #222222;
    font-size: 20px;
}

.el-upload{
    width: 80px;
    height: 100px;
}

.el-upload__text
{
    width: 80px;
    height: 100px;
}

.el-upload__input
{
    width: 80px;
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
    padding-bottom: 20px;
    border-bottom: 2px solid #ccc;
    margin-bottom: 20px;
    font-weight:bolder;
}


.user-info-cont {
    padding-left: 50px;
    flex: 1;
    font-size: 14px;
    color: #999;
}

.user-info-cont div:first-child {
    font-size: 30px;
    color: #222;
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

.todo-item {
    font-size: 14px;
}

.todo-item-del {
    text-decoration: line-through;
    color: #999;
}

.schart {
    width: 100%;
    height: 300px;
}

</style>