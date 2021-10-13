import uuid

from django.core.mail import send_mail
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import SlidingToken

from .models import ConfirmationCode, User
from .serializers import ConfirmationCodeSerializer, UserSerializer


@api_view(["POST"])
def send_email(request):
    email = request.data.get("email")
    confirmation_code = str(uuid.uuid4())
    conf_code = ConfirmationCode(
        email=email, confirmation_code=confirmation_code
    )
    conf_code.save()
    send_mail(
        "Регистрация",
        f"Ваш confirmation_code: {confirmation_code}",
        None,
        [email],
    )
    return Response({"email": email})


class RegisterView(APIView):
    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = request.data.pop("confirmation_code")
        if not ConfirmationCode.objects.filter(
            email=request.validated_data.get("email"),
            confirmation_code=confirmation_code,
        ).exists():
            return Response(
                {"confirmation_code": "Wrong confirmation_code was provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        email = request.validated_data.get("email")
        data = {"email": email, "password": confirmation_code}
        user = UserSerializer(data=data)
        user.is_valid(raise_exception=True)
        email = user.validated_data["email"]
        password = user.validated_data["password"]
        user = User.objects.get_or_create(email=email, password=password)[0]
        token = SlidingToken.for_user(user)
        return Response(data={"access": str(token)})


class AllUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ("username",)
    lookup_field = "username"
    pagination_class = PageNumberPagination

    @action(
        methods=["get", "patch"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="me",
    )
    def me(self, request):
        if request.method == "PATCH":
            serializer = UserSerializer(
                self.request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = UserSerializer(self.request.user)
        return Response(serializer.data)
