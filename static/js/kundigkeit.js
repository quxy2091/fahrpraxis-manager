const overlay=document.getElementById("overlay");

const popup=document.getElementById("popup");

const title=document.getElementById("popup-title");

const body=document.getElementById("popup-body");


function randomPosition(){

    return{

        x:50+Math.random()*1100,

        y:50+Math.random()*700

    };

}


function createStation(station){

    const p=randomPosition();

    const div=document.createElement("div");

    div.className="station";

    div.style.left=p.x+"px";

    div.style.top=p.y+"px";

    div.onclick=function(){

        popup.style.display="block";

        title.innerHTML=station.name;

        body.innerHTML=

        "<b>ID:</b> "+station.id+

        "<br><br>"

        +"Hier erscheint später"

        +"<br>"

        +"• Kundigkeit"

        +"<br>"

        +"• Strecken"

        +"<br>"

        +"• Letzte Befahrung";

    };

    overlay.appendChild(div);

}


fetch("/kundigkeit/stations/")

.then(response=>response.json())

.then(data=>{

    console.log(data.length);

    data.forEach(createStation);

});