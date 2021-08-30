from client.views import ClientViewSet, BookViewSet, ReserveViewSet
from rest_framework_extensions.routers import ExtendedSimpleRouter

router = ExtendedSimpleRouter()

router\
    .register(r'client', ClientViewSet, basename="client")\
    .register(r'books', ReserveViewSet, basename="book", parents_query_lookups=["client"])\
    .register(r'reserve', ReserveViewSet, basename="reserve", parents_query_lookups=["id", "book_id"])

router.register(r'books', BookViewSet, basename="book")

urlpatterns = router.urls
