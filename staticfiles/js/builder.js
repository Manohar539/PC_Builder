let total = 0
let build = {}

function showCategory(type, element){

document.querySelectorAll(".category-card").forEach(card=>{
card.classList.remove("active")
})

if(element){
element.classList.add("active")
}

const productList = document.getElementById("product-list")

productList.innerHTML = ""

componentsFromDB
.filter(component => component.category.toLowerCase() === type.toLowerCase())
.forEach(component=>{

productList.innerHTML += `

<div class="product-card">

<h3>${component.name}</h3>

<p class="price">€${component.price}</p>

<button onclick="addComponent('${type}','${component.name}',${component.price},'${component.socket}','${component.ram_type}',${component.power})">
Add to Build
</button>

</div>

`

})

}


function addComponent(type, name, price, socket, ram_type, power){

if(build[type]){
total -= build[type].price || 0
}

build[type] = {
name: name,
socket: socket,
ram_type: ram_type,
power: power,
price: price
}

document.getElementById(type).innerText = name

total += Number(price || 0)

document.getElementById("total").innerText = total

calculatePower()
checkCompatibility()

}


function calculatePower(){

let totalPower = 0

Object.entries(build).forEach(([type, component]) => {

if(type !== "psu" && component.power){
totalPower += Number(component.power)
}

})

document.getElementById("power").innerText = totalPower

let recommended = totalPower + 200

document.getElementById("recommended-psu").innerText = recommended

}


function checkCompatibility(){

const warningBox = document.getElementById("compatibility-warning")

warningBox.innerHTML = ""

let warnings = []

if(build.cpu && build.motherboard){
if(build.cpu.socket !== build.motherboard.socket){
warnings.push("⚠ CPU and Motherboard sockets are not compatible")
}
}

if(build.ram && build.motherboard){
if(build.ram.ram_type && build.motherboard.ram_type){
if(build.ram.ram_type !== build.motherboard.ram_type){
warnings.push("⚠ RAM type not supported by motherboard")
}
}
}

if(build.psu){
let totalPower = parseInt(document.getElementById("power").innerText) || 0
if(build.psu.power && Number(build.psu.power) < totalPower){
warnings.push("⚠ PSU may not supply enough power")
}
}

if(warnings.length > 0){
warningBox.style.color = "red"
warningBox.innerHTML = warnings.join("<br>")
}

}


function verifyBuild(){

if(!build.cpu || !build.motherboard || !build.ram){
alert("⚠ Please select CPU, Motherboard and RAM")
return false
}

checkCompatibility()

const warningBox = document.getElementById("compatibility-warning")
const warningText = warningBox.innerText.trim()

if(warningText){
alert("⚠ Build has compatibility issues:\n\n" + warningText)
return false
}

alert("✅ Build looks good!")
return true

}


// AUTO-FILL EDIT BUILD
window.onload = function(){

const firstCategory = document.querySelector(".category-card")

if(firstCategory){
showCategory("cpu", firstCategory)
}

if(typeof existingBuild !== "undefined" && existingBuild){

Object.keys(existingBuild).forEach(type => {

let component = existingBuild[type]

if(component && component.name){

addComponent(
type,
component.name,
component.price,
component.socket,
component.ram_type,
component.power
)

}

})

}

}


function getCookie(name) {

let cookieValue = null

if(document.cookie && document.cookie !== ''){

const cookies = document.cookie.split(';')

for(let i = 0; i < cookies.length; i++){

const cookie = cookies[i].trim()

if(cookie.substring(0, name.length + 1) === (name + '=')){
cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
break
}

}

}

return cookieValue

}


function saveBuild(){

if(Object.keys(build).length === 0){
alert("⚠ Build something before saving")
return
}

let params = new URLSearchParams(window.location.search)
let sector = params.get("sector") || "Gaming"

fetch(`/save-build/?sector=${sector}`, {
method: "POST",
headers: {
"Content-Type": "application/json",
"X-CSRFToken": getCookie("csrftoken")
},
body: JSON.stringify(build)
})
.then(res => res.json())
.then(data => {
alert("Build saved successfully!")
})

}


function goToCheckout(){

localStorage.setItem("build_cpu", document.getElementById("cpu").innerText)
localStorage.setItem("build_gpu", document.getElementById("gpu").innerText)
localStorage.setItem("build_ram", document.getElementById("ram").innerText)
localStorage.setItem("build_storage", document.getElementById("storage").innerText)
localStorage.setItem("build_motherboard", document.getElementById("motherboard").innerText)
localStorage.setItem("build_psu", document.getElementById("psu").innerText)
localStorage.setItem("build_case", document.getElementById("case").innerText)
localStorage.setItem("build_cooling", document.getElementById("cooling").innerText)

localStorage.setItem("build_total", document.getElementById("total").innerText)

window.location.href = "/checkout/"

}