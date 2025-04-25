const dashboard=document.getElementById('collapse');
const dash_elements=document.getElementById('dashboard-view');
const icon_description=document.getElementById('icon-description');
const icons=document.getElementsByClassName('.all-icons');

if (window.innerWidth < 900) {
    dashboard.addEventListener('click', () => {
        dash_elements.style.display = 'block';
    });
}
else {
     dashboard.addEventListener('click',()=>{
         if(icon_description.style.display==='none'){
             icon_description.style.display = 'block';
             dash_elements.style.width = '20rem';
             icon_description.style.display='flex'
             icon_description.style.flexDirection='column';
             icon_description.style.gap = '4.5rem';
         }
         else{
             icon_description.style.display = 'none';
             dash_elements.style.width = '5rem';
         }
        })
}