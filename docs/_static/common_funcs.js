const roll_dice= (dice) => {
    res= 0;
    dice[0].forEach(([n, d]) => {
        for (let i = 0; i < n; i++) res+= Math.floor(d*Math.random())+1;
    });

    return res + dice[1];
};

const decode_die_string= string => {
    let res= [];
    let modifier= 0;
    
    string.split("+").forEach(die=>{
        if (die.indexOf("d") != -1){
            let [n, d]= die.split("d",2);

            res.push([Number.parseInt(n),Number.parseInt(d)]);
        } else modifier+= Number.parseInt(die);
    });

    return [res, modifier];
};

const rpad= (string,padding_length,padding_char=" ") => {
    string= string.toString(); // Ensure no nonsense is happening
    let extra_padding= padding_length-string.length
    for (let i= 0; i < extra_padding; i++){
        string= padding_char+string;
    }

    return string
}