/** @odoo-module **/


export function storePageContext(context){
    sessionStorage.setItem("pageContext",JSON.stringify(context))
}

export function getPageContext(){
    if(sessionStorage.getItem("pageContext")){
        return JSON.parse(sessionStorage.getItem("pageContext"))
    }
    else{
        return false
    }
}

export function moveToPage(page_id,subpage_id){
    let pageContext = getPageContext()

    if(page_id!==false){
        pageContext.page_id = page_id
    }
    if(subpage_id!==false){
        pageContext.subpage_id = subpage_id
    }

    storePageContext(pageContext)
    location.reload()
}


export function storePageInfo(page_name,data){
    data.page_name = page_name
    sessionStorage.setItem("pageExtraData",JSON.stringify(data))
}

export function getPageInfo(page_name){
    if(sessionStorage.getItem("pageExtraData")){
        let data = JSON.parse(sessionStorage.getItem("pageExtraData"))
        if(data.page_name===page_name){
            return data
        }
        else{
            return undefined
        }
    }
    else{
        return undefined
    }
}

export function formatDate(date_str){
    const inputDate = date_str;

    // Split the date string (DD-MM-YYYY)
    const [year, month, day] = inputDate.split('-');
    // Create a new Date object (months are zero-based in JavaScript, so subtract 1)
    const date = new Date(`${year}-${month}-${day}`);

    // Format the date to 'MMM DD YYYY' (e.g., 'Jun 19 2025')
    const formattedDate = date.toLocaleDateString('en-US', {
        month: 'short', // Jun
        day: 'numeric', // 19
        year: 'numeric' // 2025
    });

    return formattedDate
}

export function formatDateTime(dt_str){
    dt_str = dt_str.split(" ")
    const inputDate = dt_str[0];
    let time_str = dt_str[1].split(":")

    // Split the date string (DD-MM-YYYY)
    const [year, month, day] = inputDate.split('-');
    // Create a new Date object (months are zero-based in JavaScript, so subtract 1)
    const date = new Date(`${year}-${month}-${day}`);

    // Format the date to 'MMM DD YYYY' (e.g., 'Jun 19 2025')
    const formattedDate = date.toLocaleDateString('en-US', {
        month: 'short', // Jun
        day: 'numeric', // 19
        year: 'numeric' // 2025
    });

    return time_str[0]+":"+time_str[1] + " - " + formattedDate
}