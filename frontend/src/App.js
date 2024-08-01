import React, { useEffect, useState } from 'react';
import './App.css';
import Bookings from './components/Bookings';
import BookingLoadingComponent from './components/BookingLoading';
import OrderButtons from './components/OrderButtons';

function App() {

  const BookingLoading = BookingLoadingComponent(Bookings)
  const [appState, setAppState] = useState({
    loading: false,
    bookings: null
  });

  const [order, setOrder] = useState("");

  useEffect(() => {
    setAppState({loading: true});
    const apiUrl = "http://127.0.0.1:8000/api/bookings/" + order;
    console.log(apiUrl);
    fetch(apiUrl)
      .then((response) => response.json())
      .then((bookings) => {
        setAppState({loading:false, bookings:bookings});
      });
  }, [order]);

  return (
    <div className="container">
      <h1>Flat booking App with ReactJS</h1>
      <br/>
      <div class="row">
<div class="col-12">
<div class="d-grid gap-2 d-md-flex justify-content-md-end">
  <button class="btn btn-primary active" aria-current="page" onClick={() => setOrder("")}>Default ordering</button>
  <button class="btn btn-primary" onClick={() => setOrder("?ordering=checkin")}>Order by checkin ASC</button>
  <button class="btn btn-primary"onClick={() => setOrder("?ordering=-checkin")}>Order by checkin DESC</button>
</div>
</div>
</div>
      <br/>
      <BookingLoading isLoading={appState.loading} bookings={appState.bookings} />
    </div>
  );
}

export default App;
