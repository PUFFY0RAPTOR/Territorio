function confirmacion(url){
    return confirm("Está seguro que desea eliminarlo?") ? location.href = url : console.log('No se eliminó nada')
}