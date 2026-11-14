import {useState} from "react";

function AddRides({apiUrl}){
    const [driverRoll, setDriverRoll] = useState("");
    const [fromPlace, setFromPlace] = useState("");
    const [toPlace, setToPlace] = useState("");
    const [Date, setDate] = useState("")
    const [Time, setTime] = useState("")
    const [TotalSeats, setTotalSeats] = useState("")
    const [error, setError] = useState("");
    const [msg, setMsg] = useState("");

  function handleSubmit(e){
      e.preventDefault();
      if (!driverRoll || !fromPlace || !toPlace || !Date || !Time || !TotalSeats){
          setError("All fields are required")
          return;
      }
      fetch(
      `${apiUrl}/offer_ride?driver_roll=${driverRoll}&from_place=${fromPlace}&to_place=${toPlace}&ride_date=${Date}&depart_time=${Time}&total_seats=${TotalSeats}`,
      { method: "POST" }
    )
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          setError(data.detail);
        } else {
          setMsg(`"${data.driver_roll}" added!`);
          setDriverRoll("");
          setFromPlace("");
          setToPlace("");
          setDate("");
          setTime("");
          setTotalSeats("");

        }
      });
  }
  return (
      <>
      <form className="add-form" onSubmit={handleSubmit}>
          <div>
          <label>Roll No</label>
          <input
            type="text"
            value={driverRoll}
            onChange={(e) => setDriverRoll(e.target.value)}
          />
        </div>
          <div>
              <label>From</label>
              <input
                type="text"
                value={fromPlace}
                onChange={(e) => setFromPlace(e.target.value)}
              />
          </div>
          <div>
              <label>To</label>
              <input
                type="text"
                value={toPlace}
                onChange={(e) => setToPlace(e.target.value)}
              />
          </div>
          <div>
              <label>Date</label>
              <input
                type="date"
                value={Date}
                onChange={(e) => setDate(e.target.value)}
              />
          </div>
          <div>
              <label>Depart Time</label>
              <input
                type="time"
                value={Time}
                onChange={(e) => setTime(e.target.value)}
              />
          </div>
           <div>
              <label> Total Seats</label>
              <input
                type="number"
                value={TotalSeats}
                onChange={(e) => setTotalSeats(e.target.value)}
              />
          </div>

          <button type="submit" className="btn-primary">Add Ride</button>
          {error && <p className="error">{error}</p>}
      {msg && <p className="success">{msg}</p>}
          </form>
      </>
  )
}


export default AddRides