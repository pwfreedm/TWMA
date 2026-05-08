function toggleIframe()
{
    var iframe = document.getElementById('settings');
    if(iframe.style.display == 'block') 
    {
        iframe.style.display = 'none';
    } else 
    {
        iframe.style.display = 'block';
    }
}