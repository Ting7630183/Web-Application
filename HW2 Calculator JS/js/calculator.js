let stack = [];
stack.push(0);
let entering = Boolean(true);
let bottom = 0;
let get_size = stack.length;
console.log(get_size);

function number(x){
    if(entering == true){
        normal();
        bottom = stack.pop();
        bottom = bottom * 10 + parseInt(x);
        document.getElementById("output").innerHTML = bottom;
        stack.push(bottom);
    }else{
        let size = stack.length;
        if(size >= 3){
            document.getElementById("output").innerHTML = "stack overflow";
            wrong();
            stack = [];
            stack.push(0);
            entering = true;       
        }else{
            normal();
            stack.push(0);
            entering = true;
            bottom = stack.pop();
            bottom = bottom * 10 + parseInt(x);
            document.getElementById("output").innerHTML = bottom;
            stack.push(bottom);
        }
    }  
}
function ops(x){
    //check underflow and overflow
    let size = stack.length;
    if(size < 2){
        wrong();
        document.getElementById("output").innerHTML = "stack underflow";
        stack = [];
        stack.push(0);
        entering = true;
    }else{
        correct();
        let second = stack.pop();
        let first = stack.pop();
        let result; 
        if(x === 1){
            result = first + second;
            document.getElementById("output").innerHTML = result;
            stack.push(result);
            entering = false;
        } else if(x === 2){
            result = first - second;
            document.getElementById("output").innerHTML = result;
            stack.push(result);
            entering = false;
        } else if(x === 3){
            result = first * second;
            document.getElementById("output").innerHTML = result;
            stack.push(result);
            entering = false;
        }else if(x === 4){
            if(second == 0){
                wrong();
                document.getElementById("output").innerHTML = "divide by zero";
                stack = [];
                stack.push(0);
                entering = true;
            }else{
                result = Math.floor(first / second);
                document.getElementById("output").innerHTML = result;
                stack.push(result);
                entering = false;
            }   
    }
    }   
}

function push(){
    let size = stack.length;
    if(size >= 3){
        wrong();
        document.getElementById("output").innerHTML = "stack overflow";
        stack = [];
        stack.push(0);
        entering = true;  
    }else{
        normal();
        stack.push(0);
        placement = document.getElementById("output");
        placement.innerHTML = "0";
        entering = true;
    }
    
}

function correct(){
    document.getElementById("output").style.backgroundColor = "green"; 
}

function wrong(){
    document.getElementById("output").style.backgroundColor = "red";
}
function normal(){
    document.getElementById("output").style.backgroundColor = "purple";
}

