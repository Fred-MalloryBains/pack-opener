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
    
    
    $(document).on("click", ".buy-pack-btn", function(){
        var packId = $(this).data('pack-id');
        $.ajax({
            url: '/add_pack',
            type: 'POST',
            data: JSON.stringify({ 'packId': packId }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response) {
                // Update the html rendered to reflect the opened pack items
                var resultsContainer = $('#my_packs');
                resultsContainer.empty();
                response.forEach(item => {
                    resultsContainer.append(`
                    <div class="col-md-4 d-flex align-items-stretch mb-4">
                        <div class="card"> 
                            <div class="card-body d-flex flex-column justify-content-center align-items-center">
                                <div class="card-body">
                                <h5 class="card-title">${ item.name }</h5>
                                <p class="card-text">Quantity: ${ item.quantity }</p>
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