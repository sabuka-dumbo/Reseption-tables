const select_input = document.getElementById("bookings-select");

fetch("/get_rooms/", {
    method: "POST",
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({  }),
})
.then(response => response.json())
.then(data => {
    for (const room of data.rooms) {
        const booking_div = document.createElement("div");
        booking_div.classList.add("booking");
        booking_div.innerHTML = `
            <option value="${room.id}">Room: ${room.room_number}</option>
        `;
        select_input.appendChild(booking_div);
    }

    console.log(data.bookings);
})
.catch(error => {
    console.error('Error:', error);
});