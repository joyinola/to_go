from django.urls import path
from .views import (
   
    PayForRide,
    SearchForRide,
    GoOnline,
    GoOffline,
    CreateOrder,
    VerifyPay,
    AcceptOrder,
    ListCusOrder,
    ListRiderOrder,
    ViewATrip,
    EditRoute,
    GetVehicleDetail,
    EditDriverProfile,
    UpdateTripStatus,
    DeclineOrder,
    )


urlpatterns =[
    path('search_for_ride/',SearchForRide.as_view(), name ="search-for-ride"),
    path('pay_for_ride/', PayForRide.as_view(), name="pay-for-ride"),
    path('verify_pay/', VerifyPay.as_view(),name ='verify-pay'),
    # path('pay_driver/', TripCompleted.as_view(), name="pay-driver"),
    path('rider/go_online/',GoOnline.as_view(),name = 'Go-online' ),
    path('rider/go_offline/',GoOffline.as_view(),name = 'Go-offline' ),
    path('create_order/',CreateOrder.as_view(),name = 'create-order'),
    path('list_orders/',ListCusOrder.as_view(),name = 'list-order'),
    path('list_rider_orders/',ListRiderOrder.as_view(),name = 'list-rider-order'),
    path('accept_order/',AcceptOrder.as_view(),name = 'accept-order'),
    path('view_a_trip/',ViewATrip.as_view(),name = 'view-trip'),
    path('decline_order/',DeclineOrder.as_view(),name = 'decline-order'),
    path('edit_rider_profile/',EditDriverProfile.as_view(),name = 'edit-driver'),
    path('vehicle_detail/',GetVehicleDetail.as_view(),name = 'vehicle-detail'),
    path('edit_route/',EditRoute.as_view(),name = 'edit-route'),
    path('update_trip_status/',UpdateTripStatus.as_view(),name = 'update-trip-status'),

    


]