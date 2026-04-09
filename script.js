let title = document.getElementById('title');
let price = document.getElementById('price');
let txas = document.getElementById('txas');
let ads = document.getElementById('ads');
let discont = document.getElementById('discont');
let total = document.getElementById('total');
let caont = document.getElementById('caont');
let catigore = document.getElementById('catigore');
let submit = document.getElementById('submit');

//get total
function getTotal(){

    if(price.value != ''){
        let result = ( +price.value + +txas.value + +ads.value ) 
        - +discont.value;
        total.innerHTML = result;
    total.style.background = "#040";
    }else{
        total.innerHTML = '';
        total.style.background = "#a00d02";
    }
}
//create product
let dataPro;
if(localStorage.product != null){
    dataPro = JSON.parse (localStorage.product)
}
else{
    dataPro = [];
}

submit.onclick = function()
{
 let newPro = {
    title:title.value,
    price:price.value,
    txas:txas.value,
    ads:ads.value,
    discont:discont.value,
    total:total.innerHTML,
    caont:caont.value,
    catigore:catigore.value,
 }
 if(newPro.caont > 1){
for(let i = 0; i < newPro.caont;i++){

dataPro.push(newPro);

}
 }else{
    dataPro.push(newPro);
 }
 
 // sava localstorge
 localStorage.setItem('product', JSON.stringify(dataPro) )
 clearDate()
showData()
}

//clear inputs

function clearDate(){
 title.value = '';
  price.value = '';
  txas.value = '';
  ads.value = '';
  discont.value = '';
  total.innerHTML = '';
  caont.value = '';
  catigore.value = '';
}

//red
function showData(){
let table = '';
for(let i = 0; i < dataPro.length;i++){
table += `
  <td>${i}</td>
      <td>${dataPro[i].title}</td>
      <td>${dataPro[i].price}</td>
      <td>${dataPro[i].txas}</td>
      <td>${dataPro[i].ads}</td>
      <td>${dataPro[i].discont}</td>
      <td>${dataPro[i].total}</td>
      <td>${dataPro[i].catigore}</td>
      <td><button id="update">update</button></td>
      <td><button onclick="deleteData(${i})" id="delete">delete</button></td>
    </tr>
`

}
document.getElementById('tbody').innerHTML = table;
let btnDelete = document.getElementById('deleteAll');

if(dataPro.length > 0){
btnDelete.innerHTML = `
<button onclick="deleteAll()">delete All (${dataPro.length})</button>
`

}else{
    btnDelete.innerHTML = '';
}
}
showData()

//delete

function deleteData(i){
dataPro.splice(i,1);
localStorage.product = JSON.stringify(dataPro);
showData()
}
function deleteAll(){
localStorage.clear()
dataPro.splice(0)
showData()
}

//count