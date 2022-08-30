const SELECTED_CLASS_NAME= "rolling_selected";

function isElementInViewport (el) {
    /* Lent permanently from https://stackoverflow.com/a/7557433 */
    // Special bonus for those using jQuery
    if (typeof jQuery === "function" && el instanceof jQuery) {
        el = el[0];
    }

    var rect = el.getBoundingClientRect();

    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && /* or $(window).height() */
        rect.right <= (window.innerWidth || document.documentElement.clientWidth) /* or $(window).width() */
    );
}

const split_number_repr= (string, sep) => {
    let [a, b]= string.split(sep,2);
    return [Number.parseInt(a), Number.parseInt(b)];
}
const parse_range_str= (string) => {
    return split_number_repr(string,"-");
}

const find_selected_element= (tbody, value) => {
    for (let i= 0; i < tbody.children.length; i++){
        let element= tbody.children[i];
        if (value >= element.min_value && value <= element.max_value) return element
    }
    return null;
}

const prepare_table= (tbody) => {
    for (let i= 0; i < tbody.children.length; i++){
        let element= tbody.children[i];
        [element.min_value, element.max_value]= parse_range_str(element.innerText);
    }
};
const add_randomiser= (table) => {
    let tbody= table.getElementsByTagName("tbody")[0];

    prepare_table(tbody);

    let die_text= table.getElementsByTagName("th")[0];
    let dice_info= decode_die_string(die_text.innerText);

    let die_button= document.createElement("button");
    die_button.innerText= die_text.innerText;

    die_text.innerHTML= "";
    die_text.appendChild(die_button);


    die_button.onclick= () => {
        for(let i= 0; i < tbody.children.length; i++){
            tbody.children[i].classList.remove(SELECTED_CLASS_NAME);
        }

        let res= roll_dice(dice_info);
        console.debug(`Rolled ${res}`);
        
        let selection= find_selected_element(tbody,res);
        if (selection === null){
            console.error(`Roll on ${table} failed. Could not find an element matching ${res}`);
        }
        selection.classList.add(SELECTED_CLASS_NAME);
        if (!isElementInViewport(selection)) selection.scrollIntoView();

        // Automatically trigger all rolls in the selection
        let rolls= selection.getElementsByClassName("roll");
        for (let i= 0; i < rolls.length; i++){
            rolls[i].firstChild.click();
        }
    };
};


window.addEventListener("load", ()=>{
    let roll_tables= document.getElementsByClassName("rollingtable");
    
    for (let i= 0; i < roll_tables.length; i++){
        add_randomiser(roll_tables[i]);
    }
});