const wrap_roll= node => {
    let current_timeout;

    const dice_string= node.innerText;
    const dice= decode_die_string(dice_string);

    let button= document.createElement("button");
    button.innerText= dice_string;
    
    button.onclick= () =>{
        clearTimeout(current_timeout);

        let result= roll_dice(dice);

        button.innerText= rpad(result,dice_string.length);
        current_timeout= setTimeout(()=>{
            button.innerText= dice_string;
        },1000);
    }
    
    node.innerText="";
    node.appendChild(button);
};

window.addEventListener("load", ()=>{
    let roll_texts= document.getElementsByClassName("roll")
    for (let i= 0; i < roll_texts.length; i++){
        wrap_roll(roll_texts[i]);
    }
});