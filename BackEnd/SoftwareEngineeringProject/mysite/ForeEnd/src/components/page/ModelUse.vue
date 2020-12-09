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
<!--                            <el-button style="margin-left: 10px;" size="small" type="success" @click="uploadZip">上传到服务器</el-button>-->
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

                    <el-card shadow="hover" class="mgb20" style="height:650px;">
                        <div class="user-info">
                            特征数据提取结果
                        </div>
                        <div style="width: 1000px;padding-left: 40px;padding-top: 20px;margin-top:10px;background:#c7ddef">
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

                    </el-card>

                    <el-card shadow="hover" style="height:600px;">
                        <div slot="header" class="clearfix">
                            <span>模型预测结果</span>
                        </div>
                        <div style="width: 1000px;padding-left: 40px;padding-top: 20px;margin-top:10px;background:#c7ddef">
                            <el-table
                                :data="forecastResult"
                                stripe
                                style="width: 100%"
                                border
                            >
                                <el-table-column
                                    v-for="info in ResultHeader" :key="info.key"
                                    :property="info.key"
                                    :label="info.label"
                                >
                                    <template slot-scope="scope">
                                        {{scope.row[scope.column.property]}}
                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>
                    </el-card>

                </el-col>
            </el-row>



        </div>
    </div>
</template>

<script>
export default {

    name: "ModelUse",
    baseURL:'http://localhost:8080',
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

            ResultHeader:[
                { key:"a" ,label:"稳定段总推进力"},
                { key:"b" ,label:"稳定段刀盘扭矩"},
                { key:"c" ,label:"稳定段推进速度"},
            ],

            forecastResult:[
                {
                    a:"15713.91974",
                    b:"2942.392641",
                    c:"60.83314267"
                },
                {
                    a:"15713.91974",
                    b:"2942.392641",
                    c:"60.83314267"
                },
                {
                    a:"15713.91974",
                    b:"2942.392641",
                    c:"60.83314267"
                },
                {
                    a:"15713.91974",
                    b:"2942.392641",
                    c:"60.83314267"
                },
                {
                    a:"15713.91974",
                    b:"2942.392641",
                    c:"60.83314267"
                },
                {
                    a:"15713.91974",
                    b:"2942.392641",
                    c:"60.83314267"
                },
                {
                    a:"15713.91974",
                    b:"2942.392641",
                    c:"60.83314267"
                },
                {
                    a:"15713.91974",
                    b:"2942.392641",
                    c:"60.83314267"
                },
                {
                    a:"15713.91974",
                    b:"2942.392641",
                    c:"60.83314267"
                },
                {
                    a:"15713.91974",
                    b:"2942.392641",
                    c:"60.83314267"
                },
            ],

            name: localStorage.getItem('ms_username'),
            fileList: [
                // {
                //     name:'Amonkey0.7z',
                //     url:'d:/Amonkey0.7z'
                // }
                ],
            message:"",
            colunmName: ['澳中线-悉尼-仓库', '澳中线-悉尼-仓库1'],
            totalNumber: 100,
            datas: [
                {
                list: [
                    {
                        name: '澳中线-悉尼-仓库1',
                        value: 1
                    },
                    {
                        name: '澳中线-悉尼-仓库2',
                        value: 2
                    }
                ],
                userName: 'admin'
            },
                {
                list: [
                    {
                        name: '澳中线-悉尼-仓库3',
                        value: 3
                    },
                    {
                        name: '澳中线-悉尼-仓库4',
                        value: 4
                    }
                ],
                userName: 'jason'
            }],

            number:1
        };
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
            let selectedFile=file;
            console.log(selectedFile);
            let name = selectedFile.name; //选中文件的文件名
            let size = selectedFile.size; //选中文件的大小

            console.log("文件名:" + name + "大小:" + size);



            this.$http.post(this.publicPath+'api/上传zip文件包',{file})
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
            this.$http.get(this.base+'api/获取特征数据')
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
            this.$http.get(this.base+'api/获取模型预测结果')
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