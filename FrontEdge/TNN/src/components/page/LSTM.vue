<template>
    <div>
        <div class="container">

            <el-container>
                <el-header>神经网络框架图</el-header>
                <div class="demo-image__preview">
                    <el-image
                        style="width: 100px; height: 100px;"
                        :src="url"
                        :preview-src-list="srcList">
                    </el-image>
                </div>
            </el-container>

            <el-divider></el-divider>
            <el-container>
                <el-row>
                    <span>设计思想介绍：</span>
                    <i class="el-icon-s-opportunity" style="padding-left: 2px"></i>
                </el-row>
                <br>
                <div class="introduction">
                    <span>.........</span>
                </div>
            </el-container>

            <el-divider></el-divider>
            <el-row gutter="40">
                <el-col :span="11">
                    <el-card shadow="hover" class="mgb20" style="height:252px;">
                        <div class="user-info">
                            <span>训练loss图</span>
                            <i class="el-icon-s-data" style="padding-left: 20px"></i>
                        </div>

                        <div class="user-info-list">
                            <div class="blocks">
                                <span class="demonstration">默认</span>
                                <el-image :src="src"></el-image>
                            </div>
                        </div>

                    </el-card>



                </el-col>
                <el-col :span="11">
                    <el-card shadow="hover" style="height:252px;">
                        <div slot="header" class="clearfix">
                            <span>拟合效果图</span>
                            <i class="el-icon-s-data" style="padding-left: 20px"></i>
                        </div>

                        <div class="blocks">
                            <span class="demonstration">自定义</span>
                            <el-image :src="src">
                                <div slot="placeholder" class="image-slot">
                                    加载中<span class="dot">...</span>
                                </div>
                            </el-image>
                        </div>

                    </el-card>


                </el-col>
            </el-row>




        </div>


    </div>
</template>

<script>
export default {
    name: 'LSTM',
    data() {
        return {
            url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
            srcList: [
                'https://fuss10.elemecdn.com/8/27/f01c15bb73e1ef3793e64e6b7bbccjpeg.jpeg',
                'https://fuss10.elemecdn.com/1/8e/aeffeb4de74e2fde4bd74fc7b4486jpeg.jpeg'
            ],
            src: 'https://i.postimg.cc/zDSjpbqw/Live-broadcast.jpg',
        }
    }

};
</script>

<style scoped>

.blocks{
    height: 400px;
}

.demo-image__preview{
//display: grid;
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