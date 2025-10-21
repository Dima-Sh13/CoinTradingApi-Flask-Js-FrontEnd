let objetoDePeticionDeDatosDeLaApi = new XMLHttpRequest() // Aqui se declara un objeto de json, se le tiene que pasar la "url"que tambien se llama endpoint
                                                          // que tambien se llama endpoint que se crea en routes, que debe devolver un json
let buyPetition = new XMLHttpRequest()
let sellPetiton = new XMLHttpRequest
let tradePetition = new XMLHttpRequest

// function handlerPetition_200(){}

    

function prueba(){
    let entrada = document.getElementById("prueba")

    buyPetition.open("POST","http://localhost:5000/api/prueba")
    buyPetition.onerror = function(){alert("nO HA FUNCIONADO")}
    buyPetition.send(entrada)






}