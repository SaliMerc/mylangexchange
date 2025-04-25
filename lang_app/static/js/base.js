const open_menu=document.getElementById('open-menu');
const close_menu=document.getElementById('close-menu');
const list_div=document.getElementById('list-div');
open_menu.addEventListener('click',()=>{
    list_div.style.display='block';
    close_menu.style.display='block';
    open_menu.style.display='none';
})
close_menu.addEventListener('click',()=>{
    list_div.style.display='none';
    close_menu.style.display='none';
    open_menu.style.display='block';
})