// Sends a new request to update the to-do list
function getGlobal() {
    console.log("enter get global")
    $.ajax({
        url: "/socialnetwork/get-global",
        type: "GET",
        dataType : "json",
        success: updateGlobal,
        error: updateError
    });
}

function updateError(xhr) {
    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }

    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function displayError(message) {
    $("#error").html(message);
}

function getFollower() {
    console.log("enter get global")
    $.ajax({
        url: "/socialnetwork/get-follower",
        type: "GET",
        dataType : "json",
        success: updateGlobal,
    });
}

function updateComment(id, comments){
    console.log("the id in the update comment" + id)
    
    $(comments).each(function() {
        var d = new Date(this.creation_time)
        var h = d.getHours()
        var subfix = "AM";
        if(h > 12){
            h -=12
            subfix = "PM"
        }
        dformat = [d.getMonth()+1,
            d.getDate(),
            d.getFullYear()].join('/')+' '+
           [h,
            d.getMinutes()].join(':') + ' '+
            subfix;

        console.log("enter update each comment")
        let comment_list_id = "comment_list_" + id

        if(document.getElementById("id_comment_div_" + this.id) == null){
            $("#" + comment_list_id).prepend(
                '<div id="id_comment_div_' + this.id + '">' +
                'Comment by' + ' ' + 
                '<a id="id_comment_profile_' + this.id + '"' + 'href="other_profile/' +
                this.creator_id + 
                '"'+ '>'+
                this.creator_first_name + ' ' + 
                this.creator_last_name + ' ' +
                '</a>' +
                '<a id="id_comment_text_' + this.id + '">' +
                this.text + ' ' +
                '</a>' + 
                '<a id="id_comment_date_time_' + this.id +'">' +
                dformat +
                '</a>'
            )
        }
    })
}


function updateGlobal(items) {
    console.log("enter update global in js")
    // Adds each new todolist item to the list (only if it's not already here)
    $(items).each(function() {
        var d = new Date(this.creation_time)
        var h = d.getHours()
        var subfix = "AM";
        if(h > 12){
            h -=12
            subfix = "PM"
        }
        dformat = [d.getMonth()+1,
            d.getDate(),
            d.getFullYear()].join('/')+' '+
           [h,
            d.getMinutes()].join(':') + ' '+
            subfix;

        
        let my_id_post = "id_post_div_" + this.id  
        if(document.getElementById(my_id_post) != null){
            updateComment(this.id, this.comment)

        }else if (document.getElementById(my_id_post) == null) {
            $("#post").prepend(
                '<div id="id_post_div_' + this.id + '">' +
                '<a id="id_post_profile_' + this.id + '"'+ 'href="other_profile/' +
                this.user_id + 
                '"'+ '>' + 
                'Post by ' + this.user_first_name + this.user_last_name + ' '+ 
                '</a>' + 
                '<a id="id_post_text_' + this.id + '">' +
                this.text + ' ' + 
                '</a>' +
                '<a id="id_post_date_time_'+
                this.id + '">' +
                dformat + 
                '</a>' +
                '</div>' +
                '<div id="comment_list_'+ this.id + '">' + '</div>' +
                'Comment:' + 
                '<input id="id_comment_input_text_' + this.id + '"'+
                'type="text" name="comment">' +
                '<button id="id_comment_button_'+ this.id + '"'+
                'onClick="addComment(' + this.id + ')"> Submit </buttont>' 
            )
            updateComment(this.id, this.comment)
        }    
    })
}


function addComment(id) {
    let itemTextElement = $("#id_comment_input_text_" + id)
    let itemTextValue   = itemTextElement.val()

    // Clear input box and old error message (if any)
    itemTextElement.val('')
    console.log(itemTextValue)

    $.ajax({
        url: "/socialnetwork/add-comment",
        type: "POST",
        data: "comment_text="+itemTextValue+"&post_id=" + id + "&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: updateGlobal,
        error: updateError
    });
}


function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown";
}



