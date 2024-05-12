document.addEventListener('DOMContentLoaded', function() {


    // Add event listener for the "Add Nearby Devices" button
    document.getElementById('nearbyDevicesBtn').addEventListener('click', function() {
        sendPostRequest('/api/addnearbydevices', {})
            .then(handleResponse)
            .catch(handleError);
    });

    // Add event listener for the "Set Current Date and Time" button
    document.getElementById('nearbyDevicesBtn-1').addEventListener('click', function() {
        const currentDateTime = new Date();
        sendPostRequest('/api/setdatetime', { dateTime: currentDateTime.toISOString() })
            .then(handleResponse)
            .catch(handleError);
    });

    // Add event listener for the "Clear Data" button
    document.getElementById('cleardataBtn').addEventListener('click', function() {
        if (confirm('Are you sure you want to clear the data?')) {
            sendPostRequest('/api/cleardata', {})
                .then(handleResponse)
                .catch(handleError);
        }
    });

    // Add event listener for the sensitivity level dropdown
    document.querySelector('select.form-select').addEventListener('change', function() {
        const level = this.value;
        sendPostRequest('/api/level', { level })
            .then(handleResponse)
            .catch(handleError);
    });
});

// Helper function to send POST requests
function sendPostRequest(url, data) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
}

// Helper function to handle successful responses
function handleResponse(response) {
    if (response.ok) {
        alert('Operation successful');
    } else {
        alert('Operation unsuccessful');
    }
}

// Helper function to handle errors
function handleError(error) {
    console.error('Error:', error);
    alert('An error occurred');
}