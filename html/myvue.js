const app ={
  data(){
    return{
      message:0,
      flange:[
        {"DN_公称直径":"DN100",},
        {"DN_公称直径":"DN130",},
        {"DN_公称直径":"DN140",},
        {"DN_公称直径":"DN150",}
      ]

    } //return
  }//data
}//app
Vue.createApp(app).mount('#app')