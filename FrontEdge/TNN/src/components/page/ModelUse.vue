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
                            <el-button size="small" type="primary">文件上传</el-button>
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

    name: "ModelUse",
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