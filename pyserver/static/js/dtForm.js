const dic = document.getElementById('district')
const sec = document.getElementById('sector')
const cel = document.getElementById('cell')
const vil = document.getElementById('village')
dic.addEventListener('click', function () {
    populateSector()
    clearOptions(sec)
    clearOptions(cel)
    clearOptions(vil)
})
sec.addEventListener('click', function () {
    populateCell()
    clearOptions(cel)
    clearOptions(vil)
})
cel.addEventListener('click', function () {
    populateVillage()
    clearOptions(vil)
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