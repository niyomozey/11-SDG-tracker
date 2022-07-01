const dic = document.getElementById('district')
const sec = document.getElementById('sector')
const cel = document.getElementById('cell')
const vil = document.getElementById('village')
const openNext = document.getElementById('openNext')
const search = document.getElementById('search')
var nextSelect = ''
var currentOpen = ''
var currentSelect = ''
var selectedItem = ''
var searchField = 'District'
var searchInput = ''
clearSelect()
function clearSelect(){
    sec.parentNode.style.display ='none'
    cel.parentNode.style.display ='none'
    vil.parentNode.style.display ='none'
    openNext.innerHTML = "Open Sector"
}

dic.addEventListener('click', function () {
    clearSelect()
    populateSector()
    clearOptions(sec)
    clearOptions(cel)
    clearOptions(vil)
    currentSelect = 'District'
    nextSelect = sec
    selectedItem=dic
})
openNext.addEventListener('click', function (){
    openNext.innerHTML = nextSelect == sec ? "Open Cell" : nextSelect == cel ? "Open Village" : "Open Sector";
    openNext.parentNode.style.display = nextSelect == vil ? 'none' : 'block';
    nextSelect.parentNode.style.display = 'block'
    currentSelect = nextSelect == sec ? "Sector" : nextSelect == cel ? "Cell" : "Village"
    selectedItem =  nextSelect == sec ? dic : nextSelect == cel ? sec : nextSelect == vil ? cel : vil
})
search.addEventListener('click', function(){
    searchField = currentSelect
    searchInput = selectedItem.value
    location.href = `/filter/${searchField}/${searchInput}`
})
sec.addEventListener('click', function () {
    populateCell()
    clearOptions(cel)
    clearOptions(vil)
    currentSelect = 'Sector'
    nextSelect = cel
    selectedItem = sec
})
cel.addEventListener('click', function () {
    populateVillage()
    clearOptions(vil)
    currentSelect = 'Cell'
    nextSelect = vil
    selectedItem = cel
})
function populateDistrict() {

}
async function populateSector() {
    const selectedDistrict = document.getElementById('district').value
    let sectors = await axios.post('http://localhost:3000/api/v1/rwanda/sector', {
        province: 'Kigali',
        district: selectedDistrict
    })
    console.log(sectors);
    console.log(typeof (sectors.data));
    makeOptions("sector", sectors.data)
}
async function populateCell() {
    const selectedDistrict = document.getElementById('district').value
    const selectedSector = document.getElementById('sector').value
    let sectors = await axios.post('http://localhost:3000/api/v1/rwanda/cell', {
        province: 'Kigali',
        district: selectedDistrict,
        sector: selectedSector
    })
    console.log(sectors.data);
    makeOptions("cell", sectors.data)
}
async function populateVillage() {
    const selectedDistrict = document.getElementById('district').value
    const selectedSector = document.getElementById('sector').value
    const selectedCell = document.getElementById('cell').value
    let villages = await axios.post('http://localhost:3000/api/v1/rwanda/village', {
        province: 'Kigali',
        district: selectedDistrict,
        sector: selectedSector,
        cell: selectedCell
    })
    makeOptions('village', villages.data)
}

function makeOptions(parentId, data) {
    data.forEach(element => {
        var opt = document.createElement("option");
        opt.value = element;
        opt.innerHTML = element;
        document.getElementById(parentId).appendChild(opt);
    });

}
function clearOptions(element){
    while (element.options.length) {
        element.remove(0);
    }
}