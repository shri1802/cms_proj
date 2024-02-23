from django.shortcuts import render
from user_app.serializers import ClaimUserSerializer, ClaimAdminSerializer
from user_app.models import Policy, Claim
from django.contrib.auth.models import User
from user_app.forms import PolicyForm, ClaimForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404


# Create your views here.

@api_view(['POST'])
def signup_api(request):
    print(request.method)
    if request.method == "POST":
        first_name = request.data.get("firstname")
        last_name = request.data.get("lastname")
        username = request.data.get("username")
        email = request.data.get("email")
        password1 = request.data.get("password")
        confirmpassword = request.data.get("confirmpassword")
 
        # Check if any field is empty
        if not all([first_name, last_name, username, email, password1, confirmpassword]):
            return Response({"error": "Please fill out all fields."}, status=status.HTTP_400_BAD_REQUEST)
 
        if password1 == confirmpassword:
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(
                        username=username, email=email, password=password1,
                        first_name=first_name, last_name=last_name
                    )
                    user.save()
                    return Response({"message": "Account created successfully!"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Email is already in use."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Username is already taken."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
 
@api_view(['POST'])
def login_api(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"error": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_claim_list(request):
    if request.method == 'GET':
        claims = Claim.objects.filter(user=request.user)
        serializer = ClaimUserSerializer(claims, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ClaimUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_claim_list(request):
    if request.method == 'GET':
        claims = Claim.objects.all()
        serializer = ClaimAdminSerializer(claims, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ClaimAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def admin_claim_update(request, claim_id):
    claim = get_object_or_404(Claim, claim_id=claim_id)
    serializer = ClaimAdminSerializer(claim, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_claim_delete(request, claim_id):
    try:
        claim = Claim.objects.get(claim_id=claim_id)
    except Claim.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    claim.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

