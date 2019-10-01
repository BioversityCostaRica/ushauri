function closeModal() {
    var iframe = document.getElementById("modaliframe");

    iframe.contentWindow.location.href = 'about:blank';
    setTimeout(function(){
    $('#modal1').modal('hide');
    }, 1000);
}

function showRegions(url)
{
    document.getElementById('modaliframe').src = url;
    document.getElementById("modaltitle").innerHTML = "Regions and districts";
    $('#modal1').modal('show');
}

function showGroups(url)
{
    document.getElementById('modaliframe').src = url;
    document.getElementById("modaltitle").innerHTML = "Advisory groups";
    $('#modal1').modal('show');
}

function showAudios(url)
{
    document.getElementById('modaliframe').src = url;
    document.getElementById("modaltitle").innerHTML = "Audios";
    $('#modal1').modal('show');
}

function showMenus(url)
{
    document.getElementById('modaliframe').src = url;
    document.getElementById("modaltitle").innerHTML = "IVR Menus";
    $('#modal1').modal('show');
}

function showEditQuestion(url)
{
    document.getElementById('modaliframe').src = url;
    document.getElementById("modaltitle").innerHTML = "Edit question";
    $('#modal1').modal('show');
}

function showReplyToMember(url)
{
    document.getElementById('modaliframe').src = url;
    document.getElementById("modaltitle").innerHTML = "Reply to member";
    $('#modal1').modal('show');
}

function showLanguages(url)
{
    document.getElementById('modaliframe').src = url;
    document.getElementById("modaltitle").innerHTML = "Languages";
    $('#modal1').modal('show');
}

function showUsers(url)
{
    document.getElementById('modaliframe').src = url;
    document.getElementById("modaltitle").innerHTML = "Extension agents";
    $('#modal1').modal('show');
}