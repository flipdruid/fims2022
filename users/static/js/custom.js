// /*
// const clientStatus = document.querySelector("#client_cstatus");
// const clientSpouse = document.querySelector("#client_spouse");

// clientStatus.addEventListener("click", function(e){
    
//     console.log("clientStatus.value");

// });
// */
// function hideSpouse(sps)
//     {
//         if(sps.target.value == "Married")
//             {                   
//                 document.getElementById("client_spouse").style.display="inline";
//                 document.getElementById("client_spouse_label").style.display="inline";                
//             }

//         else if(sps.target.value != "Married")
//             {                 
//                 document.getElementById("client_spouse").style.display="none";
//                 document.getElementById("client_spouse_label").style.display="none";                
//             }
//         //console.log(sps.target.value)
//     }    

window.onload = function () {
    // var month = new Array("January", "February", "March", "April",
    //     "May", "June", "July", "August", "September", "October", "November", "December");

    var today = new Date();
    
    var mm = today.getMonth()+1;
    var dd = today.getDate();    
    var yyyy = today.getFullYear();
    let current_date    = `${mm}/${dd}/${yyyy}`;
    document.getElementById('todate').innerText = current_date;
};