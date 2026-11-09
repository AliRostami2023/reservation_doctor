from rest_framework.pagination import PageNumberPagination


class MagazinePagination(PageNumberPagination):
    page_size = 15
    

class ReviewPaginations(PageNumberPagination):
    page_size = 20
