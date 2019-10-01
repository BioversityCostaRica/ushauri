function proceed()
{
    var url = $('#urlforpost').val()
    var crfToken = $('#confirmcrftoken').val()
    var form = document.createElement('form');
    form.setAttribute('method', 'post');
    form.setAttribute('action', url);
    form.style.display = 'hidden';

    var i = document.createElement("input"); //input element, text
    i.setAttribute('type',"text");
    i.setAttribute('name',"csrf_token");
    i.setAttribute('value',crfToken)
    form.appendChild(i);

    document.body.appendChild(form)
    form.submit();
}

function ShowConfirmModal(url,title,message)
{
    $('#confirm_title').html(title);
    $('#confirm_content').html(message);
    $('#urlforpost').val(url)
    $('#confirm').modal('show');
}