from rest_framework.views import APIView
from rest_framework.response import Response
from listings.models import BookingInfo
from django.db.models import Q
from django.db.models import F

class GetAvailableRoomsAPIView(APIView):

    def get(self, request):
        booking = list(BookingInfo.objects.all().values())
        if request.query_params:
            maxPrice = int(request.query_params.get('max_price'))
            check_in = request.query_params.get('check_in')
            check_out = request.query_params.get('check_out')
            qs = BookingInfo.objects.select_related().filter(
                Q(price__lte=maxPrice),
                ~Q(reservation__reserved_start_date__range=(check_in, check_out)),
                ~Q(reservation__reserved_end_date__range=(check_in, check_out))
            ).order_by('price')
            query_list = []
            for q in qs:
                if q.listing:
                    dict = {
                        "listing_type": q.listing.listing_type,
                        "title": q.listing.title,
                        "country": q.listing.country,
                        "city": q.listing.city,
                        "price": q.price
                    }
                elif q.hotel_room_type:
                    dict = {
                        "listing_type": q.hotel_room_type.hotel.listing_type,
                        "title": q.hotel_room_type.hotel.title,
                        "country": q.hotel_room_type.hotel.country,
                        "city": q.hotel_room_type.hotel.city,
                        "price": q.price
                    }
                query_list.append(dict)


            return Response(query_list)

        # serializer = BookingInfoSerializer(booking, many=True)
        # list_serializer= ListingSerializer(listing,many=True)
        return Response(booking)