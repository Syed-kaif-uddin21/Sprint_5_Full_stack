import {useState} from "react";

function RidesCard({item,apiUrl}){

    const [rollNo, setRollNo] = useState("")
    const [error, setError] = useState("");
    const [msg, setMsg] = useState("");
    const [seatsLeft, setSeatsLeft] = useState(item.seats_left);
    const [showPassenger, setShowPassenger] = useState("")

    function handle_book(){
    setError("");
    setMsg("");
    fetch(
      `${apiUrl}/book_ride?ride_id=${item.id}&roll_no=${rollNo}`,
      { method: "POST" }
    )
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          setError(data.detail);
        } else {
          setMsg("Booked!");
          setRollNo("");
          setSeatsLeft(prev = prev - 1);
        }
      });
    }

    function show_passengers(){
        setError("");
        setMsg("");
        fetch(
          `${apiUrl}/get_ride?ride_id=${item.id}`,
          { method: "GET" }
        )
          .then((res) => res.json())
          .then((data) => {
            if (data.detail) {
              setError(data.detail);
            } else {
                const names = data.map((p) => p.roll_no).join(", ");
                setShowPassenger(names || "No passengers yet");
            }
          });

    }
    return (
    <li>
        <h3>{item.driver_roll}</h3>
        <p>From : {item.from_place} --- To : {item.to_place}</p>
        <p>Date : {item.ride_date} | Time : {item.depart_time}</p>
        <p> Seats left : {seatsLeft}</p>
        <p>Status : {item.status}</p>
        <div>
             <input
          type="text"
          placeholder="Roll number"
          value={rollNo}
          onChange={(e) => setRollNo(e.target.value)}
        />
            <div><button className="rides" onClick={handle_book}>Join Ride</button>
                </div>

        </div>
        {error && <p className="error">{error}</p>}
        {msg && <p className="success">{msg}</p>}

        <div className="book-row">
            <button className="showPassengers" onClick={show_passengers}>Show Passengers</button>
            <p>{showPassenger}</p>
        </div>


    </li>
)
}

export default RidesCard

