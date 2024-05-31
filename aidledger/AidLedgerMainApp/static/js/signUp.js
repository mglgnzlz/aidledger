

document.getElementById('signup_form').addEventListener('submit', async(event) => {
    event.preventDefault();
    const ethAddress=document.getElementById('ethAddress').value;
    const userType=document.getElementById('userType').value;
    const acctName=document.getElementById('acctName').value;
    
    const response = await fetch("{% url 'signup %}", {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': '{{csrf_token}}'
        },
        body: JSON.stringify({
            ethAddress,
            userType,
            acctName,
        })
    });
    
    const data = await response.json();
    if(data.user) {
        if(data.userType == 'NGO/GOVT'){
            window.location.href = "{% url 'govGenerateQR'%}"
        }
        else if(data.userType == 'HANDLER'){
            window.location.href = "{% url 'handlerScanQR'%}"
        }
        else if(data.userType == 'RECIPIENT'){
            window.location.href = "{% url 'recipScanQR' %}"
        }
    } else {
        alert("Sign up error")
    }


});