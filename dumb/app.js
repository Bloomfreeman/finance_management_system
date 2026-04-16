window.addEventListener('pywebviewready', async function () {
    await set_text();
    await goal_data();
    await ls_cs_projection();
    await get_history();
});
async function set_text(){
        const Data= await window.pywebview.api.call()
        const data= await window.pywebview.api.refresh()

        const goal=data[1]
        const last_month_entry=data[2]
        const wage = Data[0]
        const Lsaved= Data[1]
        const Csaved= Data[2]
        const debtpayment= Data[3]
        const operation= Data[4]

        const life=last_month_entry.at(-1)[1]
        const con=last_month_entry.at(-1)[2]
        document.getElementById("monthly_income").textContent=wage
        document.getElementById("life_saving").textContent=Lsaved
        document.getElementById("a").textContent= `${goal.Life_saving_rate*100}% of income`


        document.getElementById("consumption_saving").textContent=Csaved
        document.getElementById("b").textContent= `${goal.consumption_rate*100}% of income`

        document.getElementById("debt_pay").textContent=debtpayment
        document.getElementById("c").textContent= `${goal.debt_payment_rate*100}% of consumption`

        document.getElementById("pocket_money").textContent= operation
        document.getElementById("d").textContent= `${(1-(goal.Life_saving_rate+goal.consumption_rate))*100}% of income - free to spend`

        document.getElementById("life_total").textContent=`$${life.toLocaleString('en-US')}`
        document.getElementById("cons_total").textContent=`$${con.toLocaleString('en-US')}`

        document.getElementById("per_month").textContent=`+$${(Lsaved+Csaved).toLocaleString('en-US')} added this month`
        document.getElementById("total").textContent=`$${(life+con).toLocaleString('en-US')}`
}
async function goal_data(){

const data = await window.pywebview.api.goal_data()

const lifeleft = data[0]
const consleft = data[1]
const lifepersent = data[2]
const conspersent = data[3]
const LSgoal = data[4]
const CSgoal = data[5]

createDonut("lifeDonut", lifeleft, LSgoal,lifepersent,"#37D389")
createDonut("consDonut", consleft, CSgoal,conspersent,"#6360B8")
}

const centerText = {
id: 'centerText',
afterDraw(chart, args, options) {
const {ctx, chartArea:{width, height}} = chart

ctx.save()
ctx.font = "bold 18px Segoe UI"
ctx.fillStyle = "white"
ctx.textAlign = "center"
ctx.textBaseline = "middle"

ctx.fillText(options.text, width/2, height/2)
}
}

function createDonut(id, x,y,percent,color){

new Chart(document.getElementById(id), {
type: "doughnut",
data: {
datasets: [{
data: [y-x, x],
backgroundColor: [color, "#1f2937"],
borderWidth:0
}]
},
options:{
cutout:"75%",
plugins:{
legend:{display:false},
centerText:{
text:`${percent}%`
}
}
},
plugins:[centerText]
})
}


// projection chart

async function ls_cs_projection(){
        const data = await window.pywebview.api.graph_by_year()
        const  month=data[0]
        const lprojection=data[2]
        const cprojection=data[1]

        create_projection("projection",month,lprojection,cprojection)


}

function create_projection(id,month,L,C){

const ctx = document.getElementById(id).getContext("2d")

const lifegradient = ctx.createLinearGradient(0,0,0,500)
lifegradient.addColorStop(0,"rgba(34,197,94,0.35)")
lifegradient.addColorStop(1,"rgba(34,197,94,0)")

const consgradient = ctx.createLinearGradient(0,0,0,500)
consgradient.addColorStop(0,"rgba(99,96,184,0.35)")
consgradient.addColorStop(1,"rgba(99,96,184,0)")

new Chart(ctx, {
type: "line",
data:{
labels:month,
datasets:[
{
label:"Life",
data:L,
borderColor:"#22c55e",
backgroundColor:lifegradient,
fill:'origin',
tension:0.4,
borderWidth:2,
order:2
},
{
label:"Consumption",
data:C,
borderColor:"#6360B8",
backgroundColor:consgradient,
fill:'origin',
tension:0.4,
borderWidth:2,
order:1
}
]
},
options:{
responsive:true,
maintainAspectRatio:true,
scales:{
y:{stacked:false}
}
}
})
}
// debt
new Chart(document.getElementById("debt"), {
type:"line",
data:{
labels:["Start","Q1","Q2","Q3","Q4"],
datasets:[{
data:[14400,13600,12800,12000,11200]
}]
}
})
// ---------- life history ----------
async function get_history() {
        const data= await window.pywebview.api.graph_for_the_past()
        const labels=data[0]
        const datal=data[1]
        const datac=data[2]

        history_bar("lifeHistory",labels,datal,"Life Saving History","#37D389")
        history_bar("consHistory",labels,datac,"Consumption Saving History","#6360B8")
        console.log(datac,datal)
}

function history_bar(id,labels,data,def,color){
new Chart(document.getElementById(id), {
type:"bar",
data:{
labels:labels,
datasets:[{
data:data,
label:def,
backgroundColor:color
}]
},
options:{
responsive:true,
maintainAspectRatio:false
}
})
}

// // ---------- consumption history ----------
// new Chart(document.getElementById("consHistory"), {
// type:"bar",
// data:{
// labels:["Jul","Aug","Sep","Oct","Nov","Dec",
//         "Jan","Feb","Mar","Apr","May","Jun"],
// datasets:[{
// data:[400,420,450,470,500,520,550,580,600,620,640,650],
// backgroundColor:"#3b82f6"
// }]
// },
// options:{
// responsive:true,
// maintainAspectRatio:false
// }
// })