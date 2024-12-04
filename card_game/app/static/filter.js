$(document).ready(function() {
    
    // Set the token so that we are not rejected by server
    var csrf_token = $('meta[name=csrf-token]').attr('content');
    // Configure ajaxSetup so that the CSRF token is added to the header of every request
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
    

    function fetchFiltered (){

        var isCollected = $('#isCollected').prop('checked') || false; //set default value to false 
        var rarity = $('#rarity-search').val();
        
        switch (rarity){
            case '1':
                rarity = "common";
                break;
            case '2':
                rarity = "rare";
                break;
            case '3':
                rarity = "epic";
                break;
            case '4':
                rarity = "legendary";
                break;
            default:
                rarity = "all";
        }
        console.log(isCollected)
        $.ajax({
            url: '/my_cards_query',
            type: 'POST',
            data: JSON.stringify({ 'isCollected': isCollected, 'rarity': rarity }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                
                
                // Update the html rendered to reflect the filtered cards   
                var resultsContainer = $('#query-results');
                resultsContainer.empty();
                response.forEach(item => {
                    resultsContainer.append(`
                        <div class="col-md-4 d-flex align-items-stretch mb-4">
                        <div class = ${item.rarity_class}>
                                <div class="card"> 
                                    <div class="card-body d-flex flex-column justify-content-center align-items-center">
                                        <h5 class="card-title">${ item.name }</h5> 
                                        <img src="${item.image_url}" class="card-img-top" alt="${item.name}" /> 
                                        <p class="card-text">Rarity: ${ item.rarity }</p> 
                                        <p class="card-text">Genre: ${ item.genre }</p> 
                                    </div>
                                </div> 
                            </div>
                         </div>
                    `);
                });
            },
            error: function(error) {
                console.log(error);
            }
        });
        console.log("Fetching filtered results");

    }
    $("#check").on("change", fetchFiltered);
    $("#rarity-search").on("change", fetchFiltered);
    fetchFiltered();   
});