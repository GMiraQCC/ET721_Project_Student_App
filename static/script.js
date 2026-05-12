function validatePasswordLength(){
    const password = document.querySelector('input[name="password"]').value
    
    if (password.length < 6){
        alert("Passowrd must be at least 6 characters long!")
        return false
    }

    return true
}