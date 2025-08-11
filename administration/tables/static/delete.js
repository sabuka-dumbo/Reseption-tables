const select_input = document.getElementById("bookings-select");

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
            <option value="${booking.id}">Room: ${booking.room.room_number} ${booking.guest_name}</option>
        `;
        select_input.appendChild(booking_div);
    }

    console.log(data.bookings);
})
.catch(error => {
    console.error('Error:', error);
});