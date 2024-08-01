import React from 'react';

const OrderButtons = () => {
    return (
   
<div class="row">
<div class="col-12">
<div class="btn-group">
  <a href="#" class="btn btn-primary active" aria-current="page">Default ordering</a>
  <a href="#" class="btn btn-primary">Order by checkin ASC</a>
  <a href="#" class="btn btn-primary">Order by checkin DESC</a>
</div>
</div>
</div>
    );
};

export default OrderButtons;