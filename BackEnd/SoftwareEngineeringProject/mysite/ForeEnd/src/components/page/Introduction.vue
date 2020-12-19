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
                    <div>&emsp;&emsp;随着“一带一路”倡议的推进，我国对中西部地
                        区公路、铁路等交通基础设施的投资力度不断加大，
                        这极大的促进了以全断面隧道掘进机(TBM)为主要
                        施工方式的深长隧道开挖技术的发展
                    </div>
                    <div>&emsp;&emsp;TBM 的高效掘进与施工安全一直是相关人员
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
                    <div>&emsp;&emsp;除了围岩质量，TBM 的掘进效率也很大程度上依赖于掘进参数的选择。
                        TBM 设备是各种复杂系统的组合，它的性能很大程度上依赖于刀盘切削性能与推进压力。
                    </div>
                    <div>&emsp;&emsp;优化这两个掘进参数，可以促进TBM挖掘的掘进效率</div>
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
                    <div>&emsp;&emsp;首先区分掘进过程的上升段和稳定段，剔除异常数据，为后期建模提供良好的基础.</div>
                    <div>&emsp;&emsp;搭建多个神经网络模型，对比分析预测结果，选出最好的模型.</div>
                    <div>&emsp;&emsp;利用最优模型分析预测，来帮助确定掘进时合适的掘进参数.</div>
                </div>

                <el-col :offset="1" :span="18" style="margin-top: 60px">

                    <div class="sub-title">Model</div>

                    <div class="demo-basic--circle" style="margin-left: 30px;margin-top:20px">

                        <div class="block" >
                            <div id="1Model" style="float: left">
                                <button class="ButtonCss"
                                        style="width:200px;height:200px;border-radius:100px 100px 100px 100px"
                                        @click="handleSelect('/TNN')"
                                ></button>
                            </div>
                            <div class="labeltitle" >
                                <label for="1Model">TNN</label>
                            </div>
                        </div>

                        <div class="block">
                            <div id="2Model" style="float: left">
                                <button class="ButtonCss"
                                    style="width:200px;height:200px;border-radius:100px 100px 100px 100px"
                                    @click="handleSelect('/LSTM')"
                                >
                                </button>
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


.sub-title{
    color:white;
    font-size: 30px;
    height: 50px;
    font-weight: bolder;
    text-shadow: 0 0 10px #fff,
    0 0 20px #fff, 0 0 30px #fff,
    0 0 40px #ff00de, 0 0 70px #ff00de,
    0 0 80px #ff00de, 0 0 100px #ff00de,
    0 0 150px #ff00de;
}
/*.ButtonCss{*/
/*    z-index: 1;*/
/*    color: white;*/
/*    background: #40a9ff;*/
/*    outline: none;*/
/*    border: none;*/
/*    padding: 0.5em 1em;*/
/*}*/

/*.ButtonCss:hover {*/
/*    cursor: pointer;*/
/*    animation: jelly 0.5s;*/
/*}*/

/*.ButtonCss {*/
/*    outline: none;*/
/*    border: none;*/
/*    z-index: 1;*/
/*    position: relative;*/
/*    color: white;*/
/*    background: #40a9ff;*/
/*    padding: 0.5em 1em;*/
/*}*/


/*.ButtonCss::before {*/
/*    width:200px;height:200px;border-radius:100px 100px 100px 100px;*/
/*    content: "";*/
/*    z-index: -1;*/
/*    position: absolute;*/
/*    top: 0;*/
/*    bottom: 0;*/
/*    left: 0;*/
/*    right: 0;*/
/*    background-color: #fa541c;*/
/*    transform-origin: center;*/
/*    transform: scaleY(0);*/
/*    transition: transform 0.4s ease-in-out;*/
/*}*/

/*.ButtonCss:hover {*/
/*    cursor: pointer;*/
/*}*/

/*.ButtonCss:hover::before {*/
/*    transform-origin: center;*/
/*    transform: scaleY(1);*/
/*}*/

/*.ButtonCss{*/
/*    outline: none;*/
/*    border: none;*/
/*    cursor: pointer;*/
/*    color: white;*/
/*    position: relative;*/
/*    background-color: #40a9ff;*/
/*    z-index: 1;*/
/*    overflow: hidden;*/
/*}*/

/*.ButtonCss::before {*/
/*    z-index: -1;*/
/*    content: "";*/
/*    position: absolute;*/
/*    top: 50%;*/
/*    left: 50%;*/
/*    width: 1em;*/
/*    height: 1em;*/
/*    border-radius: 50%;*/
/*    background-color: #f18640;*/
/*    transform-origin: center;*/
/*    transform: translate3d(-50%, -50%, 0) scale(0, 0);*/
/*    transition: transform 0.35s ease-in-out;*/
/*}*/

/*.ButtonCss:hover::before {*/
/*    transform: translate3d(-50%, -50%, 0) scale(16, 16);*/
/*}*/

.ButtonCss {
    position: relative;
    z-index: 1;
    border: none;
    outline: none;
    padding: 0.5em 1em;
    color: white;
    background-color: #1890ff;
}

.ButtonCss:hover {
    cursor: pointer;
}

.ButtonCss::before {
    width:200px;height:200px;border-radius:100px 100px 100px 100px;
    content: "";
    position: absolute;
    z-index: -1;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    border: 4px solid #1890ff;
    transform: scale(1);
    transform-origin: center;
}

.ButtonCss:hover::before {
    transition: all 0.75s ease-out;
    border: 1px solid#e6f7ff;
    transform: scale(1.25);
    opacity: 0;
}







@keyframes jelly {
    0%,
    100% {
        transform: scale(1, 1);
    }

    33% {
        transform: scale(0.9, 1.1);
    }

    66% {
        transform: scale(1.1, 0.9);
    }
}

@keyframes jelly {
    0%,
    100% {
        transform: scale(1, 1);
    }

    25%,
    75% {
        transform: scale(0.9, 1.1);
    }

    50% {
        transform: scale(1.1, 0.9);
    }
}



.block{
    float: left;
    height: 250px;
    width: 400px;
    margin-left: 100px;
}


.labeltitle{
    float: left;
    height: 40px;
    line-height: 40px;
    text-align: center;
    width: 150px;

    text-shadow:#FF0000 0 0 10px;
    color:white;
    font-size:60px;

    /*color: #dd6161;*/
    /*background: #2d8cf0;*/
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


</style>
