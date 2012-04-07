
function file_rows(rows) {
    var file_row_cycle=2;
    var strr='';
    for(var i in rows) {
        strr+=file_row(rows[i],file_row_cycle++%2+1);
    }
    $('#filerows').html(strr);
    //$('#filerows').fadeIn();
    // TODO: Ajax-loader background ausblenden
    $('#loader').hide();
}

function file_row(data,rownr) {
    var row = '\
    <div class="filerow filerow'+ rownr +'" id="filerow-'+data['id']+'">\
        <div class="name" style="padding:2px;text-align:left;">\
            <a href="'+ data['datei'] +'" target="_blank">'+ data['name'] +'</a>\
            <sup>('+ data['endung'].substring(1) +')</sup>';
    if(user_is_staff) {
        row += '\
            <div style="float:right;">';
        if(data['gesichtet']=="False") row += '\
                <a href="javascript:review('+data['id']+');">\
                    <img src="/admin/media/img/admin/icon-yes.gif" alt="als gesichtet markieren"/>\
                </a>';
        row += '\
                <a href="/admin/lernhilfen/lernhilfe/'+ data['id'] +'/">\
                    <img src="/admin/media/img/admin/icon_changelink.gif" alt="Bearbeiten/Löschen" />\
                </a>\
            </div>';
    }

    row +='\
            <div style="clear:both;"></div>\
        </div>\
        <div class="meta">\
            <span>'+ data['studiengang'] +'</span>\
            <span>'+ data['modul'] +'</span>\
            <span>'+ data['dozent'] +'</span>\
            <span>'+ data['semester'] +'</span>\
            <span>'+ data['art'] +'</span>\
            <div style="clear:both;"></div>\
        </div>\
    </div>\
    ';
    return row;
}

function get_filter_vals() {
    filter =  {
        'studiengang':$('#id_studiengang').val(),
        'modul':$('#id_modul').val(),
        'dozent':$('#id_dozent').val(),
        'semester':$('#id_semester').val(),
        'art':$('#id_art').val(),
        'offset':offset,
    };
    if(user_is_staff && $('#show_unreviewed').attr('checked')) 
        filter['ungesichtet']=true;
    return filter;
}

function parse_response(response) {
    if(response['has_next']) $('#btn_nextpage').show();
    else $('#btn_nextpage').hide();

    if(response['has_prev']) $('#btn_prevpage').show();
    else $('#btn_prevpage').hide();

    file_rows(response['rows']);

}


function request_filerows(l_offset) {
    if(!l_offset) offset=0;
    else offset = l_offset;
    $.get( '/lernhilfen/get/',get_filter_vals(),parse_response );
    // 2. suchanfrage stellen und anntwort-funktion als callback setzen
    // 3. ajax-loader bild anzeigen
    $('#loader').fadeIn();
    //$('#filerows').hide();
}

function review(id) {
    $('#filerow-'+id).css({'background-color':'#080'});
    $.get( '/lernhilfen/sichten/'+id,review_callback);
}

function callback_filter_change() {
    request_filerows();
}

function review_callback() {
    request_filerows();
}

// Optional:
// Hash-url auswerten

// Ablauf beim laden der seite:
// 1. Optional: hash auswerten
// 2. suchanfrage stellen und anntwort-funktion als callback setzen
// 3. ajax-loader bild anzeigen

request_filerows();

$('.filter select').select(callback_filter_change);
$('#show_unreviewed').select(callback_filter_change);

$('#btn_hochladen').click( function() {
    $('#ulform1').fadeToggle(500)
    $('#ulform2').delay(300).fadeToggle(500)
    return false;
}
);

$('#btn_nextpage').click(function () {
    request_filerows(offset+1);
});

$('#btn_prevpage').click(function () {
    request_filerows(offset-1);
});
