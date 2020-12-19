<template>
    <div>
        <div class="container">

            <el-container>
                <el-header>神经网络框架图</el-header>
                <div class="demo-image__preview">
                    <el-image
                        style="width: 600px; height: 600px;"
                        :src="lstmurl"
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
                    <div>&emsp;&emsp;LSTM是RNN的一个变种，RNN的每一次隐含层的计算结果都与当前输入以及上一次的隐含层结果相关。
                        通过这种方法，RNN的计算结果便具备了记忆之前几次结果的特点。</div>
                    <div>&emsp;&emsp;LSTM的特点就是在RNN结构以外添加了各层的阀门节点。LSTM模型的记忆功能就是由这些阀门节点实现的。
                        当阀门打开的时候，前面模型的训练结果就会关联到当前的模型计算，而当阀门关闭的时候之前的计算结果就不再影响当前的计算。</div>
                    <div>&emsp;&emsp;因此，通过调节阀门的开关我们就可以实现早期序列对最终结果的影响。而当你不不希望之前结果对之后产生影响，
                        比如自然语言处理中的开始分析新段落或新章节，那么把阀门关掉即可。</div>
                </div>
            </el-container>

            <el-divider></el-divider>

            <el-row gutter="40">

                <el-col :span="12">
                    <el-card shadow="hover" class="mgb20" style="height:552px;">
                        <div class="user-info">
                            <span>训练loss图</span>
                            <i class="el-icon-s-data" style="padding-left: 20px"></i>
                        </div>

                        <div class="user-info-list">
                            <div class="blocks">
                                <span class="demonstration">默认</span>
                                <el-image :src="img3"></el-image>
                            </div>
                        </div>
                    </el-card>
                </el-col>

                <el-col :span="12">
                    <el-card shadow="hover" style="height:552px;">
                        <div slot="header" class="clearfix">
                            <span>拟合效果图</span>
                            <i class="el-icon-s-data" style="padding-left: 20px"></i>
                        </div>

                        <div class="blocks">
                            <span class="demonstration">自定义</span>
                            <el-image :src="img4">
                                <div slot="placeholder" class="image-slot">
                                    加载中<span class="dot">...</span>
                                </div>
                            </el-image>
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
export default {
    name: 'LSTM',
    data() {
        return {
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

            lstmurl: require('@/assets/img/模型图-LSTM-AM.png'),
            srcList: require("@/assets/img/模型图-LSTM-AM.png"),

            img3:require('@/assets/img/Loss1.png'),
            img4:require('@/assets/img/Loss2.png'),
        }
    },
    mounted() {
        let myChart1=this.$echarts.init(document.getElementById('myEchart1'));
        let myChart2=this.$echarts.init(document.getElementById('myEchart2'));
        let myChart3=this.$echarts.init(document.getElementById('myEchart3'));

        myChart1.setOption(this.option1);
        myChart2.setOption(this.option1);
        myChart3.setOption(this.option1);
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