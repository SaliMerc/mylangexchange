const dashboard=document.getElementById('collapse');
const dash_elements=document.getElementById('dashboard-view');
const icon_description=document.getElementById('icon-description');
const icons=document.getElementsByClassName('.all-icons');
const main_content=document.getElementById('main-content');
const search_form=document.getElementById('search-submit');


if (window.innerWidth < 900) {
    dashboard.addEventListener('click', () => {
        dash_elements.style.display = 'block';
    });
}
else {
     dashboard.addEventListener('click',()=>{
         if(icon_description.style.display==='none'){
             icon_description.style.display = 'block';
             dash_elements.style.width = '23rem';
             icon_description.style.display='flex'
             icon_description.style.flexDirection='column';
             icon_description.style.gap = '3rem';
             main_content.style.marginLeft='23rem';
         }
         else{
             icon_description.style.display = 'none';
             dash_elements.style.width = '5rem';
             main_content.style.marginLeft='5rem';
             main_content.style.width='90%';
         }
        })
}