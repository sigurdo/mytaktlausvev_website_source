window.onload = function(){

    document.querySelectorAll('.autocompleteselect').forEach((el)=>{
        let settings = {
            allowEmptyOption: true,
        };
            new TomSelect(el,settings);
        });
    }
        