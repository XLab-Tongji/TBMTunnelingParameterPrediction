<template>
    <el-container>
        <el-header style="text-align:center; font-size:30px">
            <span>TBM掘进参数预测模型</span>
        </el-header>


        <el-collapse v-model="activeNames" @change="handleChange">

            <el-collapse-item name="1">

                <template slot="title">
                    <div style="width: 40px"></div>
                    <div class="buttontitle">
                        <el-button type="success">工程背景 Background</el-button>
                    </div>
                    <i class="header-icon el-icon-info"></i>
                </template>

                <div class="IntroTest">
                    <div>随着“一带一路”倡议的推进，我国对中西部地
                        区公路、铁路等交通基础设施的投资力度不断加大，
                        这极大的促进了以全断面隧道掘进机(TBM)为主要
                        施工方式的深长隧道开挖技术的发展
                    </div>
                    <div>TBM 的高效掘进与施工安全一直是相关人员
                        最为关心的问题。相较于传统钻爆法，TBM 具有施
                        工快速、安全、自动化程度高等优点，但同时
                        它也对于地质条件更加敏感；岩土不确定性与不良
                        地质条件是 TBM 掘进过程中面临的主要风险。
                    </div>
                </div>

            </el-collapse-item>

            <el-collapse-item name="2">
                <template slot="title">
                    <div style="width: 40px"></div>
                    <div class="buttontitle">
                        <el-button type="warning">研究意义 research significance</el-button>
                    </div>
                    <i class="header-icon el-icon-s-flag"></i>
                </template>
                <div class="IntroTest">
                    <div>除了围岩质量，TBM 的掘进效率也很大程度上依赖于掘进参数的选择。
                        TBM 设备是各种复杂系统的组合，它的性能很大程度上依赖于刀盘切削性能与推进压力。
                    </div>
                    <div>优化这两个掘进参数，可以促进TBM挖掘的掘进效率</div>
                </div>
            </el-collapse-item>

            <el-collapse-item name="3">
                <template slot="title" span="12">

                    <div style="width: 40px"></div>
                    <div class="buttontitle" style="border-left: 50px">
                        <el-button type="danger">研究方法 research method</el-button>
                    </div>
                    <i class="header-icon el-icon-star-on"></i>

                </template>
                <div class="IntroTest">
                    <div>首先区分掘进过程的上升段和稳定段，剔除异常数据，为后期建模提供良好的基础.</div>
                    <div>搭建多个神经网络模型，对比分析预测结果，选出最好的模型.</div>
                    <div>利用最优模型分析预测，来帮助确定掘进时合适的掘进参数.</div>
                </div>

                <el-col :offset="2" :span="12">

                    <div class="sub-title" >Model</div>
                    <div class="demo-basic--circle">

                        <div class="block" >
                            <div style="float: left">
                            <el-avatar id="1Model"
                                       :size="200"
                                       src="circleUrl"
                                       @click.native="handleSelect('/TNN')"></el-avatar>
                            </div>
                            <div class="labeltitle" >
                                <label for="1Model">TNN</label>
                            </div>

                        </div>

                        <div class="block">
                            <div style="float: left">
                                <el-avatar id="2Model"
                                       :size="200"
                                       src="circleUrl"
                                       @click.native="handleSelect('/LSTM')"></el-avatar>
                            </div>
                            <div class="labeltitle" >
                                <label for="2Model">LSTM+AM</label>
                            </div>

                        </div>

                    </div>

                </el-col>


            </el-collapse-item>

        </el-collapse>
    </el-container>


</template>

<script>
export default {

    data() {
        const item = {
            name: 'Introduction',
            temp: 'Introduction',
        };
        return {
            tableData: Array(8).fill(item),
            activeNames: ['1'],
            circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
        };
    },


    methods: {
        handleSelect(key){
            if(key!=='') {
                console.log(key);
                this.$router.push({path:key})
            }
        },

        handleChange(val) {
            console.log(val);
        }
    }
};
</script>

<style scoped>
.block{
    float: left;
    height: 250px;
    width: 400px;
    border-top: 20px;
}


.labeltitle{
    float: left;
    font-size: 20px;
    height: 40px;
    line-height: 40px;
    text-align: center;
    width: 150px;
    color: #dd6161;
    background: #2d8cf0;
    border-top: 20px;
}

.el-header {
    background-color: #B3C0D1;
    color: #222222;
    height: 50px;
    line-height: 50px;
}

.el-aside {
    color: #333;
}

.buttontitle {
    width: 300px;
}


.IntroTest {
    font-size: 20px;
    padding-left: 20px;
}
.sub-title{
    font-size: 20px;
    height: 50px;

}


</style>

<!--                <el-col :span="5" style="background: #00a854;width: 150px;height: 300px">-->
<!--                    <div class="grid-content bg-purple-dark">-->
<!--                        <el-form-item label-width="120px">-->

<!--                        <span slot="label">-->
<!--                            <span class="span-box">-->
<!--                                <span>主食 ：</span>-->
<!--                            <i class="el-icon-tableware ico-pre"></i>-->
<!--                            </span>-->
<!--                        </span>-->

<!--&lt;!&ndash;                            <el-radio v-model="" label="1">饺子</el-radio>&ndash;&gt;-->
<!--&lt;!&ndash;                            <el-radio v-model="" label="2">米饭</el-radio>&ndash;&gt;-->
<!--                        </el-form-item>-->
<!--                    </div>-->
<!--                </el-col>-->