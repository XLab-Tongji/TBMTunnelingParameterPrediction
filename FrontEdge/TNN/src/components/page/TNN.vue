<template>
    <div>
        <div class="container">

            <el-container>
                <el-header>神经网络框架图</el-header>
                <div class="demo-image__preview">
                    <el-image
                        :src="url"
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
                    <span>借鉴NNRF树结构的思想，把特征分组输入不同的神经网络，
                        再借鉴DLA的思想，把结果进行aggression，
                        最后由一个神经网络综合所有的结果得出最终的结果</span>
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
                                <el-image :src="FittingDiagram"></el-image>
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
                            <el-image :src="LossDiagram">
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
//import model1 from'@/assets/img/Tan1.png';


export default {
    name: 'TNN',
    data() {
        return {
            url:require('@/assets/img/Tan1.png'),
            srcList: [
                require('@/assets/img/Tan1.png'),
            ],

            FittingDiagram:'https://i.postimg.cc/zDSjpbqw/Live-broadcast.jpg',
            LossDiagram:'https://i.postimg.cc/zDSjpbqw/Live-broadcast.jpg',
            fit:'scale-down'
        }
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




</style>