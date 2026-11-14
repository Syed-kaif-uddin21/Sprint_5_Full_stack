import { useState, useEffect } from "react";
import RidesCard from "./components/RidesCard.jsx";
import AddRides from "./components/OfferAride.jsx";
import "./App.css";

const API_URL = "http://127.0.0.1:8001";

const allowed = ["", "main_gate", "hostels", "bus_stand", "railway_station", "airport", "tech_park"];

function App() {
  const [Ride, setRide] = useState([]);
  const [FromFilter, setFromFilter] = useState("");
  const [ToFilter, setToFilter] = useState("");
  const [DateFilter, setDateFilter] = useState("");

  function loadRides(from, to, date) {
    let url = `${API_URL}/get_rides`;
//  host:/
    if (from && to && date) {
      url += `?from_location=${from}&to_location=${to}&date=${date}`;
    } else if (from && to) {
      url += `?from_location=${from}&to_location=${to}`;
    } else if (from && date) {
      url += `?from_location=${from}&date=${date}`;
    } else if (to && date) {
      url += `?to_location=${to}&date=${date}`;
    } else if (from) {
      url += `?from_location=${from}`;
    } else if (to) {
      url += `?to_location=${to}`;
    } else if (date) {
      url += `?date=${date}`;
    }

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setRide(data);
        } else {
          setRide([]);
        }
      });
  }

  useEffect(() => {
    loadRides(FromFilter, ToFilter, DateFilter);
  }, [FromFilter, ToFilter, DateFilter]);

  return (
    <>
      <div className="app-header">
        <h1>Carpool Booking</h1>
        <div className="filter-row">
          <label>From:</label>
          <select value={FromFilter} onChange={(e) => setFromFilter(e.target.value)}>
            {allowed.map((t) => (
              <option key={t} value={t}>{t === "" ? "All" : t}</option>
            ))}
          </select>

          <label>To:</label>
          <select value={ToFilter} onChange={(e) => setToFilter(e.target.value)}>
            {allowed.map((t) => (
              <option key={t} value={t}>{t === "" ? "All" : t}</option>
            ))}
          </select>

          <label>Date:</label>
          <input
            type="date"
            value={DateFilter}
            onChange={(e) => setDateFilter(e.target.value)}
          />
        </div>
      </div>

      <ul className="equipment-list">
        {Ride.map((item) => (
          <RidesCard
            key={item.id}
            item={item}
            apiUrl={API_URL}
            onRefresh={() => loadRides(FromFilter, ToFilter, DateFilter)}
          />
        ))}
      </ul>

      <div>
        <h2>Offer a Ride</h2>
      </div>
      <div className="section">
        <AddRides apiUrl={API_URL} onRefresh={() => loadRides(FromFilter, ToFilter, DateFilter)} />
      </div>
    </>
  );
}

export default App;