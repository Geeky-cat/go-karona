var keys = Object.keys(data);
keys.forEach(function(domain) {
    var value = data[domain]; 
    var paths=Object.keys(value);
    create("DOMAIN",domain,"",paths,"")

})


function create(type,name,path,paths,param){
    var li=document.createElement("li")
    var span=document.createElement("span")
    var a=document.createElement("a")
    var i=document.createElement("i")
    var ul=document.createElement("ul")
    if(type==="DOMAIN")
    {
        var text=""
        li.className="alert alert-primary"
        i.className="icon-folder-open"
        a.href=name
        a.target="_blank"
        a.innerText="🔗"
        span.appendChild(i)
        span.innerText=name
        span.appendChild(a)
        li.appendChild(span)
        paths.forEach(function(path){
            if(path!="")
                text+=create("PATH",name,path,paths,param)
    
        })
        ul.innerHTML=text
        li.appendChild(ul)
        document.getElementById("tsi").appendChild(li)

    }
    if(type==="PATH")
    {
        var text=""
        var params=data[name][path]
        params.forEach(function(parameter){
            if(parameter!="")
            {
             text+=create("PARAM",name,path,paths,parameter)
            }
        })
        ul.innerHTML=text
        li.className="alert alert-dark"
        i.className="icon-minus-sign"
        a.href=name+path
        a.target="_blank"
        a.innerText="🔗"
        span.appendChild(i)
        span.innerText=path
        span.appendChild(a)
        li.appendChild(span)
        li.appendChild(ul)
        return li.outerHTML   
    }
    if(type==="PARAM")
    {
        li.className="alert alert-success"
        i.className="icon-leaf"
        a.href=name+path+param
        a.target="_blank"
        a.innerText="🔗"
        span.appendChild(i)
        span.innerText=param
        span.appendChild(a)
        li.appendChild(span)
        return li.outerHTML

    }

}
