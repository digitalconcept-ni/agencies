var preloader = document.querySelector('#preloader');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var pathname = window.location.pathname;

const csrftoken = getCookie('csrftoken');

function message_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}

function message_info(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        $.each(obj, function (key, value) {
            html += ` <span class='text-center'> ${value}</span>`;
        });
    } else {
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        template: 'material',
        confirmButtonColor: "#3085d6",
        title: 'info',
        html: html,
        icon: 'info'
    });
}

function submit_with_ajax(url, title, content, parameters, callback) {

    Swal.fire({
        title: title,
        text: content,
        icon: "info",
        showCancelButton: true,
        confirmButtonColor: "#198754",
        cancelButtonColor: "#d33",
        confirmButtonText: "Si",
        cancelButtonText: "No"
    }).then((result) => {
        if (result.isConfirmed) {
            // Agregamos el preloader al bosy
            document.body.prepend(preloader);
            $.ajax({
                url: url,
                data: parameters,
                type: 'POST',
                dataType: 'json',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                processData: false,
                contentType: false,
                success: function (request) {
                    // Quitamos el preloader cuando se haya cumplido la accion
                    if (preloader) {
                        preloader.remove();
                    }

                    // if (request.hasOwnProperty('info')) {
                    //     message_info(request.info);
                    //     callback(request);
                    //     return false;
                    // }
                    if (!request.hasOwnProperty('error')) {
                        callback(request);
                        return false;
                    } else {
                        message_error(request.error);
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    message_error(errorThrown + ' ' + textStatus);
                }
            });
        }

    });
}

function alert_action(title, content, callback, cancel) {

    Swal.fire({
        title: title,
        text: content,
        icon: "info",
        showCancelButton: true,
        confirmButtonColor: "#198754",
        cancelButtonColor: "#d33",
        confirmButtonText: "Si",
        cancelButtonText: "No"
    }).then((result) => {
        if (result.isConfirmed) {
            callback();
        }
    })

    // $.confirm({
    //     theme: 'material',
    //     title: title,
    //     icon: 'fa fa-info',
    //     content: content,
    //     columnClass: 'small',
    //     typeAnimated: true,
    //     cancelButtonClass: 'btn-primary',
    //     draggable: true,
    //     dragWindowBorder: false,
    //     buttons: {
    //         info: {
    //             text: "Si",
    //             btnClass: 'btn-primary',
    //             action: function () {
    //                 callback();
    //             }
    //         },
    //         danger: {
    //             text: "No",
    //             btnClass: 'btn-red',
    //             action: function () {
    //                 cancel();
    //             }
    //         },
    //     }
    // })
}

function validate_form_text(type, event, regex) {
    var key = event.keyCode || event.which;
    var numbers = (key > 47 && key < 58) || key === 8;
    var numbers_spaceless = (key > 47 && key < 58);
    var letters = !((key !== 32) && (key < 65) || (key > 90) && (key < 97) || (key > 122 && key !== 241 && key !== 209 && key !== 225 && key !== 233 && key !== 237 && key !== 243 && key !== 250 && key !== 193 && key !== 201 && key !== 205 && key !== 211 && key !== 218)) || key === 8;
    var letters_spaceless = !((key < 65) || (key > 90) && (key < 97) || (key > 122 && key !== 241 && key !== 209 && key !== 225 && key !== 233 && key !== 237 && key !== 243 && key !== 250 && key !== 193 && key !== 201 && key !== 205 && key !== 211 && key !== 218)) || key === 8;
    var decimals = ((key > 47 && key < 58) || key === 8 || key === 46);

    if (type === 'numbers') {
        return numbers;
    } else if (type === 'numbers_spaceless') {
        return numbers_spaceless;
    } else if (type === 'letters') {
        return letters;
    } else if (type === 'numbers_letters') {
        return numbers || letters;
    } else if (type === 'letters_spaceless') {
        return letters_spaceless;
    } else if (type === 'letters_numbers_spaceless') {
        return letters_spaceless || numbers_spaceless;
    } else if (type === 'decimals') {
        return decimals;
    } else if (type === 'regex') {
        return regex;
    }
    return true;
}

function validate_decimals(el, evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode;
    var number = el.val().split('.');

    if (charCode !== 46 && charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    } else if (number.length > 1 && charCode === 46) {
        return false;
    } else if (el.val().length === 0 && charCode === 46) {
        return false;
    }

    return true;
}

function formatNumber(value) {
    return new Intl.NumberFormat('es-NI', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    }).format(value);
}

/**
 * Preloader
 */
if (preloader) {
    window.addEventListener('load', () => {
        preloader.remove();
    });
}

// Get ystem year

// var year = new Date;
// let spanYear = document.getElementById('year-system');
// spanYear.innerHTML = `${year.getFullYear()}`;

// function toggleFullScreen() {
//   if (!document.fullscreenElement &&    // alternative standard method
//       !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement ) {  // current working methods
//     if (document.documentElement.requestFullscreen) {
//       document.documentElement.requestFullscreen();
//     } else if (document.documentElement.msRequestFullscreen) {
//       document.documentElement.msRequestFullscreen();
//     } else if (document.documentElement.mozRequestFullScreen) {
//       document.documentElement.mozRequestFullScreen();
//     } else if (document.documentElement.webkitRequestFullscreen) {
//       document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
//     }
//   } else {
//     if (document.exitFullscreen) {
//       document.exitFullscreen();
//     } else if (document.msExitFullscreen) {
//       document.msExitFullscreen();
//     } else if (document.mozCancelFullScreen) {
//       document.mozCancelFullScreen();
//     } else if (document.webkitExitFullscreen) {
//       document.webkitExitFullscreen();
//     }
//   }
// }