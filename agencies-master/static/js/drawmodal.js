const drawModal = (data) => {
    if (data.hasOwnProperty('modalHeaderBody')) {
        let modalHeader = $(`#modalheader div[rel="modal-header"]`).empty();
        modalHeader.append(data.modalHeaderBody)
    }
    if (data.hasOwnProperty('modalBodyBody')) {
        let modalBody = $(`#modalbody div[rel="modal-body"]`).empty();
        modalBody.append(data.modalBodyBody)
    }
    if (data.hasOwnProperty('modalFooterBody')) {
        let modalFooter = $(`#modalfooter div[rel="modal-footer"]`).empty();
        modalFooter.append(data.modalFooterBody);
    }
    // $('#modalInfo2').modal('show');
}