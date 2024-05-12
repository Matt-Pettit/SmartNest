// Get the necessary elements
const downloadDataBtn = document.getElementById('downloaddataBtn');
const beginDateInput = document.getElementById('begindate');
const endDateInput = document.getElementById('enddate');
const picturesCheckbox = document.getElementById('formcheck-pictures');
const videosCheckbox = document.getElementById('formcheck-videos');
const tempsCheckbox = document.getElementById('formcheck-temps');
const humidityCheckbox = document.getElementById('formcheck-humidity');
const outputFormatSelect = document.getElementById('output-format');

// Add event listener to the button
downloadDataBtn.addEventListener('click', () => {
  const beginDate = beginDateInput.value;
  const endDate = endDateInput.value;
  const pictures = picturesCheckbox.checked;
  const videos = videosCheckbox.checked;
  const temps = tempsCheckbox.checked;
  const humidity = humidityCheckbox.checked;
  const outputFormat = outputFormatSelect.value;

  if (beginDate === "" || endDate === "") {
    window.alert("Dates cannot be empty.");
  } else {
    // Create the data object to send in the POST request
    const data = {
      beginDate,
      endDate,
      pictures,
      videos,
      temps,
      humidity,
      outputFormat
    };

    alert('The system will now generate your data and automatically download it for you once it is ready. Please do not leave this page.');

    // Send the POST request to /api/gendata
    fetch('/api/gendata', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json()) // Parse the response as JSON
    .then(data => {
      // Check if the response has a 'status' of 'success' and a 'zipfile' property
      if (data.status === 'success' && data.zipfile) {
        // Construct the URL for the zipfile
        const currentUrl = new URL(window.location.href);
        const zipfileUrl = `${currentUrl.origin}/${data.zipfile}`;

        // Redirect the user to the zipfile URL
        window.location.href = zipfileUrl;
      } else {
        // Handle unsuccessful response
        console.log('Server response:', data);
        alert('There was an error. Please try again later.');
      }
    })
    .catch(error => {
      // Handle any errors that occurred during the request
      console.error('Error:', error);
      alert('There was an error');
    });
  }
});