const container_div = document.getElementById("bookings-container");

fetch("/get_bookings/", {
    method: "POST",
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({  }),
})
.then(response => response.json())
.then(data => {
    for (const booking of data.bookings) {
        const booking_div = document.createElement("div");
        booking_div.classList.add("booking");
        booking_div.innerHTML = `
            <p>Room: ${booking.room}</p>
        `;
        container_div.appendChild(booking_div);
    }

    console.log(data.bookings);
})
.catch(error => {
    console.error('Error:', error);
});