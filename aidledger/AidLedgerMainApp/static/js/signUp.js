document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signup-form');
    
    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        // Example MetaMask connection code
        if (typeof window.ethereum !== 'undefined') {
            try {
                const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
                const ethAddress = accounts[0];
                document.getElementById('ethAddress').value = ethAddress;
                
                form.submit();
            } catch (error) {
                console.error('MetaMask connection error:', error);
                alert('Failed to connect to MetaMask');
            }
        } else {
            alert('MetaMask is not installed. Please install it to continue.');
        }
    });
});