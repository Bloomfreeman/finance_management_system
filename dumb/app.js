window.addEventListener('pywebviewready', function () {
    loadHistory()
});

async function loadHistory(){

const data = await window.pywebview.api.get_total()

const lifeleft = data[0]
const consleft = data[1]
const lifepersent = data[2]
const conspersent = data[3]
const LSgoal = data[4]
const CSgoal = data[5]

createDonut("lifeDonut", lifeleft, LSgoal,lifepersent)
createDonut("consDonut", consleft, CSgoal,conspersent)
console.log(lifeleft, consleft, lifepersent, conspersent, LSgoal, CSgoal)
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

function createDonut(id, x,y,percent){

new Chart(document.getElementById(id), {
type: "doughnut",
data: {
datasets: [{
data: [y-x, x],
backgroundColor: ["#22c55e", "#1f2937"],
borderWidth:0
}]
},
options:{
cutout:"75%",
plugins:{
legend:{display:false},
centerText:{
text:percent
}
}
},
plugins:[centerText]
})
}
loadHistory()


// projection chart
new Chart(document.getElementById("projection"), {
type: "line",
data:{
labels:["Jan","Feb","Mar","Apr","May","Jun"],
datasets:[
{
label:"Life",
data:[21000,22000,23000,24000,24500,24700]
},
{
label:"Consumption",
data:[9000,10000,11000,12000,13000,13720]
}
]
}
})

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
new Chart(document.getElementById("lifeHistory"), {
type:"bar",
data:{
labels:["Jul","Aug","Sep","Oct","Nov","Dec",
        "Jan","Feb","Mar","Apr","May","Jun"],
datasets:[{
data:[700,750,800,820,860,900,920,940,960,970,975,975],
backgroundColor:"#22c55e"
}]
},
options:{
responsive:true,
maintainAspectRatio:false
}
})


// ---------- consumption history ----------
new Chart(document.getElementById("consHistory"), {
type:"bar",
data:{
labels:["Jul","Aug","Sep","Oct","Nov","Dec",
        "Jan","Feb","Mar","Apr","May","Jun"],
datasets:[{
data:[400,420,450,470,500,520,550,580,600,620,640,650],
backgroundColor:"#3b82f6"
}]
},
options:{
responsive:true,
maintainAspectRatio:false
}
})