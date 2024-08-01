import React from "react";

function BookingLoading(Component){
    return function BookingLoadingComponent({isLoading, ...props}) {
        if (!isLoading) return <Component {...props} />;
        return (
            <p style={{fontSize: '25px'}}>
                Waiting for the data to load!...
            </p>
        )
    }
}

export default BookingLoading;