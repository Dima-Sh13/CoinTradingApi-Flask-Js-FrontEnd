console.log("Se vincula bien")
let show_movements = new XMLHttpRequest()
let buyPetition = new XMLHttpRequest()
let sellPetiton = new XMLHttpRequest()
let tradePetition = new XMLHttpRequest()
let exchangePetition = new XMLHttpRequest()

// function handlerPetition_200()


function movements(){
    show_movements.open("GET","/api/v1/movimientos");
    show_movements.onload = show_movements_handler;
    show_movements.onerror = function(){alert("No se ha podido completar la peticion de movimientos")}
    show_movements.send();
}

function exchange(){
    let moneda_a_cambiar = document.getElementById("moneda_from_form");
    let moneda_to = document.getElementById("moneda_to_form");
    
    
    exchangePetition.open("GET",`/api/v1/${moneda_a_cambiar}/${moneda_to}`);
    exchangePetition.onload = exchange_rate
    exchangePetition.onerror = function(){alert("No se ha podido completar la peticion de movimientos")};
    exchangePetition.send();
}
    





function show_movements_handler(){
    if(this.readyState === 4){//para verificar si es una peticion http
        if(this.status === 200){//es para saber si el estado de codigo es el correcto 
            //alert(this.responseText);//formato string
            const movimientos = JSON.parse(this.responseText)//convertir string a lista de json
            //datos [{obj1},{obj2}]
            //{ data: [{obj1},{obj2}], status:"Ok"}
            const datos = movimientos.data;
            //limpiar la tabla
            //document.getElementById("movements_table").innerHTML="<tr><th>Id</th><th>Fecha</th><th>Concepto</th><th>Cantidad</th></tr>"
           

            if (datos.length===0){
                
                let tabla = document.getElementById("movements_table");

                const fila = document.createElement("tr");

                const celda_vacia = document.createElement("td");
                celda_vacia.innerHTML = "No hay registros de movimientos."
                fila.appendChild(celda_vacia);
                tabla.appendChild(fila);

            }else{

                let tabla = document.getElementById("movements_table");

                for( let i =0;datos.length;i++){

                    const fila = document.createElement("tr");

                    const celda_time = document.createElement("td");
                    celda_time.innerHTML = datos[i].date + datos[i].time;
                    fila.appendChild(celda_time);

                    const celda_moneda_from = document.createElement("td");
                    celda_moneda_from.innerHTML = datos[i].moneda_from;
                    fila.appendChild(celda_moneda_from);

                    const celda_amount_from = document.createElement("td");
                    celda_amount_from.innerHTML = datos[i].amount_from;
                    fila.appendChild(celda_amount_from);

                    const celda_moneda_to = document.createElement("td");
                    celda_moneda_to.innerHTML = datos[i].moneda_to;
                    fila.appendChild(celda_moneda_to);

                    const celda_amount_to = document.createElement("td");
                    celda_moneda_to.innerHTML = datos[i].celda_amount_to;
                    fila.appendChild(celda_amount_to);

                    tabla.appendChild(fila);

                }

            }

        }else{
            alert("Se ha producido un error en la consulta http")
        }
    }
}

function viewForm(){
    document.getElementById('trading_form').style.display="block";
}

function hideForm(){
    limpiarCampos();
    document.getElementById('trading_form').style.display="none";
}

function buyMovement(){
    const moneda_from = document.getElementById('moneda_from_form').value;
    const amount_from = document.getElementById('amount_from_form').value;
    const moneda_to = document.getElementById("moneda_to_form").value
    const amount_to = document.getElementById('amount_to_form').value;

    //control de ingreso de datos
    if(moneda_from === ""){
        alert("Debes agregar un concepto");
        return
    }
    if(amount_from == 0){
        alert("Debes agregar cantidad positiva");
        return
    }
    

    buyPetition.open("POST","/api/v1/compra");
    // buyPetition.onload = buyPetition_handler  
    buyPetition.onerror = function(){alert(" es aqui donde falla")}
    buyPetition.setRequestHeader("Content-Type","application/json")  

    //definir la estructura json y enviar
    const data_json = JSON.stringify(
        {
        "moneda_to":moneda_to,
        "amount_from":amount_from,
        "moneda_from":moneda_from,
        "amount_to":amount_to,
        }
        
    )
    console.log("por aqui pasa")
    buyPetition.send( data_json );
}

function buyPetition_handler(){
    if(this.readyState === 4){//para verificar si es una peticion http
        if(this.status === 200){//es para saber si el estado de codigo es el correcto 
           
            console.log("Registro correcto!");
            //limpiar inputs
            /*
            //ocultar formulario
            hideForm();
            //refrescar lista  
            
            show_movements.open("GET","/api/v1/movimientos");
            show_movements.onload = show_movements_handler
            show_movements.onerror = function(){alert("No se ha podido completar la peticion de movimientos")}
            show_movements.send(); 
            */

        }else{
            alert("Se ha producido un error al intentar registrar el movimiento");
        }
    }
}



function exchange_rate(){
    const exchange_coin_rate = JSON.parse(this.responseText)
    const valor_calculado = exchange_coin_rate.data
    let valor_a_cambiar = document.getElementById("amount_from_form");
    let valor_a_recibir = document.getElementById("amount_to_form")
    valor_a_recibir.innerHTML = valor_calculado





}

window.onload = function(){
    //movements()
    let buy = document.getElementById("btn-buy");
    buy.addEventListener("click", viewForm)
   
    let alta =  document.getElementById("btn-alta");
    alta.addEventListener("click", buyMovement)
    
    exchangePetition.open("GET", "")
    
}

















