function confirmacion(url){
    return confirm("Está seguro que desea eliminarlo?") ? location.href = url : console.log('No se eliminó nada')
}

function buscarAprendices(url){
    //location.href = url;

    dato = $('#dato_buscar').val();
    resultado = $('#respuesta');

    token = $('input[name="csrfmiddlewaretoken"]').val();
    console.log("Token: " + token);


    //console.log( dato );

    /*let post_data= {
        'csrfmiddlewaretoken':"{{ csrf_token }}"
    }
    console.log(post_data);
    */

    $.ajax({
        url: url,
        type: 'POST',
        data: { "dato_buscar": dato, "csrfmiddlewaretoken" : token }, //Primer dato es el name
        //dataType: 'json' En caso de que se vaya a recibir un JSON
        success: (res) => {
            resultado.html(res);
            //respuesta.innerHTML = respuesta; Equivalente a lo de arriba
        }, 
        error: (error) => {
            console.log("Error " + error);
        }
    });

    //AJAX
}