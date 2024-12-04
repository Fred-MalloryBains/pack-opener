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
    

    $("#open-pack-btn").on("click", function() {
        var packId = $(this).data('pack-id');
        console.log("Opening pack with id: " + packId);
        $.ajax({
            url: '/open_pack_response',
            type: 'POST',
            data: JSON.stringify({ 'packId': packId }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                $('.card').remove();
                var gifElement = $('<img>', {
                    id: 'loading-gif',
                    src: '/static/images/explosion.gif', //gif open source from https://giphy.com/gifs/explosion-3o7TKz5vzv3zWg6ZqA
                    alt: 'Loading...',
                    style: 'width: 100%; height: 100%; object-fit: cover; display: block; margin: 0 auto; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);'
                });
                
                $('body').append(gifElement);
            
                // Show the GIF
                function showGif() {
                    $('#loading-gif').show();
                }
            
                // Hide the GIF
                function hideGif() {
                    $('#loading-gif').hide();
                }
                showGif();
                setTimeout(hideGif, 900);
                
            // Update the html rendered to reflect the opened pack items
                var resultsContainer = $('#pack-results');
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
    });
});