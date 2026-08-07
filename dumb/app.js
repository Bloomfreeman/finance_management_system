 // Keep track of which button was clicked
let currentUpdate = "";

// Open popup
function openModal(type) {

        currentUpdate = type;

        const modal = document.getElementById("updateModal");
        const title = document.getElementById("modalTitle");
        const description = document.getElementById("modalDescription");
        const label = document.getElementById("inputLabel");
        const input1 = document.getElementById("input1");
        const input2 = document.getElementById("input2");
        const input3 = document.getElementById("input3");
        const input4 = document.getElementById("input4");
        const input5 = document.getElementById("input5");

        if (type === "income") {

        title.textContent = "Update Income";
        description.textContent =
                "Enter your new monthly income.";

        // label.textContent = "Monthly Income";

        input1 .placeholder = "wage";
        input2.placeholder = "current life saving";
        input3.placeholder = "current consumption saving";
        input4.placeholder = "debt";
        input5.style.display = "none";

        } else if (type === "goal") {
        input5.style.display = "block";
        title.textContent = "Update Savings Goal";
        description.textContent =
                "Enter your new savings goal.";

        // label.textContent = "Savings Goal";

        input1.placeholder = "Life Saving Goal";
        input2.placeholder = "consumption Saving Goal";
        input3.placeholder = "Life Saving persentage EX: 0.1-1.0";
        input4.placeholder = "consumption Saving persentage EX: 0.1-1.0";
        input5.placeholder = "debt payment rate EX: 0.1-1.0";
        }

        input1.value = "";
        input2.value = "";
        input3.value = "";
        input4.value = "";
        input5.value = "";

        modal.style.display = "flex";

        input1.focus();
        input2.focus();
        input3.focus();
        input4.focus();
        input5.focus();
}


// Close popup
function closeModal() {

        document.getElementById("updateModal").style.display = "none";

}


// Save the new value
function saveUpdate() {

        let value = document.getElementById("input1").value.trim();
        let input2Value = document.getElementById("input2").value.trim();
        let input3Value = document.getElementById("input3").value.trim();
        let input4Value = document.getElementById("input4").value.trim();
        let input5Value = document.getElementById("input5").value.trim();


        let num = value === ""? null : Number(value);
        let num2 = input2Value === ""? null : Number(input2Value);
        let num3 = input3Value === ""? null : Number(input3Value);
        let num4 = input4Value === ""? null : Number(input4Value);
        let num5 = input5Value === ""? null : Number(input5Value);

        // if (Number(value) <= 0 || Number(input2Value) <= 0 || Number(input3Value) <= 0 || Number(input4Value) <= 0 || Number(input5Value) <= 0) {

        // alert("Please enter a valid amount.");

        // return;
        // }


        // Update income
        if (currentUpdate === "income") {
        update_Data(wage=num,currentLs=num2,currentCs=num3,debt=num4)
        // document.getElementById("incomeDisplay")
        //         .textContent = "$" + formattedValue;

        }


        // Update savings goal
        if (currentUpdate === "goal") {
        update_Json(lsgoal=num,csgoal=num2,lsrate=num3,csrate=num4,debrate=num5)

        }


        // Close popup
        closeModal();
}


// Close when clicking outside popup
window.onclick = function(event) {

        const modal =
        document.getElementById("updateModal");

        if (event.target === modal) {

        closeModal();

        }
}



window.addEventListener('pywebviewready', async function () {
    await set_text();
    await goal_data();
    await ls_cs_projection();
    await get_history();
    await debt_projection();

});
async function save_data(){
        await window.pywebview.api.save()
        location.reload();
}

async function update_Json(lsgoal,csgoal,lsrate,csrate,debrate){
        await window.pywebview.api.update_json(LSgoal=lsgoal, CSgoal=csgoal, Life_saving_rate=lsrate, consumption_rate=csrate, debt_payment_rate=debrate)
        location.reload();

}

async function update_Data(wage,currentLs,currentCs,debt){
        await window.pywebview.api.update_Data(wage=wage, currentLs=currentLs, currentCs=currentCs, debt=debt)
        location.reload();
       }

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

        const life=Data[5]
        const con=Data[6]
        // const life=last_month_entry.at(-1)[1]
        // const con=last_month_entry.at(-1)[2]
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
        
        document.getElementById("life_total-y").textContent=`$${(Lsaved*12).toLocaleString('en-US')}`
        document.getElementById("cons_total-y").textContent=`$${(Csaved*12).toLocaleString('en-US')}`
        document.getElementById("combined_total-y").textContent=`$${(Lsaved*12+Csaved*12).toLocaleString('en-US')}`

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
cutout:"40%",
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
async function debt_projection(){
    const data = await window.pywebview.api.graph_by_month()
    const  month=data[0]
    const debt=data[3]
        create_debt_projection("debt",month,debt)
}

function create_debt_projection(id,month,debt){

new Chart(document.getElementById(id), {
type:"line",
data:{
labels:month,
datasets:[{
data:debt,
label:"Debt Left",
borderColor:"#ef4444",
backgroundColor:"rgba(239,68,68,0.35)",
fill:'origin',
tension:0.4,
borderWidth:2
}]
}
})}
// ---------- life history ----------
async function get_history() {
        const data= await window.pywebview.api.graph_for_the_past()
        const labels=data[0]
        const datal=data[1]
        const datac=data[2]

        history_bar("lifeHistory",labels,datal,"Life Saving History","#37D389")
        history_bar("consHistory",labels,datac,"Consumption Saving History","#6360B8")
        // console.log(datac,datal)
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