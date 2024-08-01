import React, { useEffect, useState } from 'react';

const Bookings = (props) => {

    const { bookings } = props;

    if (!bookings || bookings.length === 0) return <p>Can not find any bookings, sorry</p>;

    return (

            <div class="row">
            <div class="col">
            <table class="table">
  <thead>
    <tr>
      <th scope="col">Flat name</th>
      <th scope="col">Id</th>
      <th scope="col">Checkin</th>
      <th scope="col">Checkout</th>
      <th scope="col">Previous Booking Id</th>
    </tr>
  </thead>
  <tbody>
  {bookings.map((booking) => {
    return (<tr key={booking.id}>
      <th scope="row">{booking.flat_name}</th>
      <td>{booking.id}</td>
      <td>{booking.checkin}</td>
      <td>{booking.checkout}</td>
      <td>{booking.previous_booking_id}</td>
    </tr>
    );
})
  }
  </tbody>
</table>
</div>
</div>

 
    );
};

export default Bookings;