
let show_movements = new XMLHttpRequest()
let buyPetition = new XMLHttpRequest()
let tradePetition = new XMLHttpRequest()





function movements(){
    show_movements.open("GET","/api/v1/movimientos");
    show_movements.onload = show_movements_handler;
    show_movements.onerror = function(){alert("No se ha podido completar la peticion de movimientos")}
    show_movements.send();
}

function showPurchaseModal() {
    
    const modalElement = document.getElementById('purchaseModal');
    
    const modal = new bootstrap.Modal(modalElement);
    
    modal.show();
}

function calcularConversion() {
    
    const coin_from = (document.getElementById("moneda_from_form") || {}).value;
    const coin_to   = (document.getElementById("moneda_to_form")   || {}).value;
    const amount_from = (document.getElementById("amount_from_form") || {}).value;

    if (!coin_from || !coin_to || !amount_from) {
        alert("Por favor completa todos los campos antes de calcular.");
        return;
    }

    const amountNum = Number(String(amount_from).replace(",", "."));
    if (!isFinite(amountNum) || amountNum <= 0) {
        alert("Introduce una cantidad válida mayor que 0.");
        return;
    }

    
    const exchangePetition = new XMLHttpRequest();
    const url = `/api/v1/tasa/${encodeURIComponent(coin_from)}/${encodeURIComponent(coin_to)}`;

    exchangePetition.open("POST", url, true);
    exchangePetition.setRequestHeader("Content-Type", "application/json");

    exchangePetition.onload = function () {
        if (exchangePetition.status >= 200 && exchangePetition.status < 300) {
            try {
                const data = JSON.parse(exchangePetition.responseText);
                // aceptar ambas claves por compatibilidad
                const purchased = data.purchasedAmount ?? data.purchased_amount ?? null;
                if (purchased === null) {
                    console.error("Respuesta inesperada:", data);
                    alert("Respuesta inesperada del servidor (comprueba consola).");
                    return;
                }
                // asignar al input (si es input .value funciona)
                const out = document.getElementById("amount_to");
                

                if (out) out.value = purchased;
                purchaseModal()
                showPurchaseModal()

            } catch (err) {
                console.error("Error parseando JSON:", err, exchangePetition.responseText);
                alert("Respuesta inválida del servidor");
            }
        } else {
            console.error("Petición fallida:", exchangePetition.status, exchangePetition.statusText);
            alert("Error en la petición al servidor: " + exchangePetition.status);
        }
    };

    exchangePetition.onerror = function () {
        console.error("Error de red o petición abortada");
        alert("No se pudo conectar con el servidor.");
    };

    // enviar JSON con el amount como número
    const payload = { amount: amountNum };
    exchangePetition.send(JSON.stringify(payload));
    

}

function show_movements_handler(){
    if(this.readyState === 4){//para verificar si es una peticion http
        if(this.status === 200){//es para saber si el estado de codigo es el correcto 
            //alert(this.responseText);//formato string
            const movimientos = JSON.parse(this.responseText)//convertir string a lista de json
            //datos [{obj1},{obj2}]
            //{ data: [{obj1},{obj2}], status:"Ok"}
            const datos = movimientos.datos;
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
                    celda_time.innerHTML = datos[i][0];
                    fila.appendChild(celda_time);

                    const celda_moneda_from = document.createElement("td");
                    celda_moneda_from.innerHTML = datos[i][1];
                    fila.appendChild(celda_moneda_from);

                    const celda_amount_from = document.createElement("td");
                    celda_amount_from.innerHTML = datos[i][2];
                    fila.appendChild(celda_amount_from);

                    const celda_moneda_to = document.createElement("td");
                    celda_moneda_to.innerHTML = datos[i][3];
                    fila.appendChild(celda_moneda_to);

                    const celda_amount_to = document.createElement("td");
                    celda_amount_to.innerHTML = datos[i][4];
                    fila.appendChild(celda_amount_to);

                    const celda_unit_price = document.createElement("td");
                    celda_unit_price.innerHTML = datos[i][5];
                    fila.appendChild(celda_unit_price);

                    tabla.appendChild(fila);

                }

            }

        }else{
            alert("Se ha producido un error en la consulta http")
        }
    }
}

function viewForm(){
    document.getElementById('conversion_form').style.display="block";
}

function hideForm(){
    
    document.getElementById('conversion_form').style.display="none";
}

function buyMovement(){
    const moneda_from = document.getElementById('moneda_from_form').value;
    const amount_from = document.getElementById('amount_from_form').value;
    const moneda_to = document.getElementById("moneda_to_form").value;
    const amount_to = document.getElementById('amount_to').value;

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
    
    buyPetition.send( data_json );
    alert("Compra Realizada!")
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
function cleanModal() {
    // cogemos todos los valores del formulario y el modal
    const moneda_from = document.getElementById('moneda_from_form');
    const amount_from = document.getElementById('amount_from_form');
    const moneda_to = document.getElementById('moneda_to_form');
    const amount_to = document.getElementById('amount_to');
    
    const model_moneda_from = document.getElementById("coin_from_modal");
    const model_amount_from = document.getElementById("amount_from_modal");
    const model_moneda_to = document.getElementById("coin_to_modal");
    const model_amount_to = document.getElementById("amount_to_modal");;

    
    // los vaciamos al cancelar la operacion
    model_moneda_from.textContent = '';
    model_amount_from.textContent = '';
    model_moneda_to.textContent = '';
    model_amount_to.textContent = '';

    moneda_from.value = "";
    amount_from.value = "";
    moneda_to.value = "";
    amount_to.value = "";

}
function purchaseModal() {
    // Valores del formulario
    const moneda_from = document.getElementById('moneda_from_form').value;
    const amount_from = document.getElementById('amount_from_form').value;
    const moneda_to = document.getElementById('moneda_to_form').value;
    const amount_to = document.getElementById('amount_to').value;

    // Los del modal
    const model_moneda_from = document.getElementById("coin_from_modal");
    const model_amount_from = document.getElementById("amount_from_modal");
    const model_moneda_to = document.getElementById("coin_to_modal");
    const model_amount_to = document.getElementById("amount_to_modal");

    // Limpieza de modal
    model_moneda_from.textContent = '';
    model_amount_from.textContent = '';
    model_moneda_to.textContent = '';
    model_amount_to.textContent = '';

    // Rellenado d modal
    model_moneda_from.textContent = moneda_from;
    model_amount_from.textContent = amount_from;
    model_moneda_to.textContent = moneda_to;
    model_amount_to.textContent = amount_to;
}

function status_info() {
    let invested = document.getElementById("invested_info");
    let recovered = document.getElementById("recovered_info");
    let valor_compra = document.getElementById("valor_compra_info");
    let wallet_value = document.getElementById("wallet_value");

    const statusPetition = new XMLHttpRequest()

    statusPetition.open("GET","/api/v1/status")
    statusPetition.onload = function () {
        const data = JSON.parse(statusPetition.responseText);

        invested.textContent = data.invested;
        recovered.textContent = data.recovered;
        valor_compra.textContent = data.valorCompra;
        wallet_value.textContent = data.wallet_value;

    }
    statusPetition.onerror = function () {
        alert("No se ha podido recuperar el estado de inversion")
    }
    statusPetition.send()
        


}

window.onload = function(){
   
    movements()

    let boton = document.getElementById("formBtn")
    boton.addEventListener("click",viewForm)
    boton.addEventListener("dblclick", hideForm)
   
    let purchase_Btn =

}



















