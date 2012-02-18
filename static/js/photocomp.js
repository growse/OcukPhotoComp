$.widget( "custom.catcomplete", $.ui.autocomplete, {
                _renderMenu: function( ul, items ) {
                    var self = this,
                    currentCategory = "";
                    var catheader = $(document.createElement('li'));
                    catheader.addClass('ui-autocomplete-category');

                    $.each( items, function( index, item ) {
                        if ( item.category != currentCategory ) {
                            catheader.clone().text(item.category).appendTo(ul);
                            currentCategory = item.category;
                        }
                        self._renderItem( ul, item );
                    });
                }
            });

            $(function() {
                var cache = {},
                lastXhr;
                $( "#searchbox" ).catcomplete({
                    minLength: 2,
                    select: function(event, ui) { 
                        if (ui.item.season!=null) {
                            window.location = "/rounds/"+ui.item.season+"/"+ui.item.value+"/"; return false;
                        } else {
                            window.location = "/people/"+ui.item.value+"/"; return false;
                        }
                    },
                    source: function( request, response ) {
                        var term = request.term;
                        if ( term in cache ) {
                            response( cache[ term ] );
                            return;
                        }

                        lastXhr = $.getJSON( "/searchhelper/"+term+"/", request, function( data, status, xhr ) {
                            cache[ term ] = data;
                            if ( xhr === lastXhr ) {
                                response( data );
                            }
                        });
                    }
                }).keydown(function(e){
                    if (e.keyCode === 13){
                        $("#searchbox").trigger('submit');
                    }
                });
            });

function selectImage(id,seasonname,roundtheme,score,personname) {
	var imageurl = "http://ocukimages1.growse.com/";
        var caption = roundtheme +"("+seasonname+") - Score: "+score;
        var fullcaption = "<a href=\"/rounds/"+seasonname+"/"+roundtheme+"/#"+personname+"\">"+roundtheme+" ("+seasonname+")</a> - Score: "+score;
        $('#selected img').attr("src",imageurl+id+"_"+seasonname+"_"+roundtheme+"_"+personname+"_MEDIUM.jpg");
        $('#selected img').attr("alt",caption);
        $('#selected a').attr("href",imageurl+id+"_"+seasonname+"_"+roundtheme+"_"+personname+"_FULL.jpg");
        $('#selected a').attr("title",caption);
        $('#selectedcaption').html(fullcaption);
}

