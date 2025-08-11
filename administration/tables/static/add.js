const select_input = document.getElementById("bookings-select");

fetch("/get_rooms/", {
    method: "POST",
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({}),
})
.then(response => response.json())
.then(data => {
    for (const room of data.rooms) {
        console.log(room.id);
        const option = document.createElement("option");
        option.value = room.id;
        option.textContent = `Room: ${room.room_number}`;
        select_input.appendChild(option);
    }
})
.catch(error => {
    console.error('Error:', error);
});
