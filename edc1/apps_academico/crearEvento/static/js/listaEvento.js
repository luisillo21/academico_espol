$(document).ready(function(){
   
    $("input#buscar").click(function(event){
        event.preventDefault();
        var texto=$("input#buscador").val();
        if(texto.lenght != 0){
            var eventos=$("#contenido #evento").filter(function(index){
                $(this).show()
                var evento=$(this).text()
                if(evento.indexOf(texto) == -1){
                    $(this).hide();
                }
            });
        }else{
            $("div#contenido").each(function(){
                $(this).show();
            });
        }
    });
});