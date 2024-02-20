from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Policy, Claim
from .forms import PolicyForm, ClaimForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def signin(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            return render(request, 'user_app/signin.html', {'error': 'Invalid credentials'})
        
    return render(request, 'user_app/signin.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if User.objects.filter(username=username).exists():
            return render(request, 'user_app/register.html', {'error': 'User already exists, please login instead.'})
        else:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            return redirect('signin')       
    return render(request, 'user_app/register.html')

def signout(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'user_app/home.html')


@login_required
def main(request):
    user = request.user
    fnuser = user.first_name

    # Determine if the user is an admin
    is_admin = user.is_staff

    if is_admin:
        claims = Claim.objects.all()  # Admin sees all claims
        policies = Policy.objects.all()  # Admin sees all policies
    else:
        claims = Claim.objects.filter(user=user)  # Normal user sees their own claims
        policies = Policy.objects.filter(user=user)  # Normal user sees their own policies

    # Count claims with different statuses
    total_accepted = claims.filter(status='A').count()
    total_rejected = claims.filter(status='B').count()
    total_pending = claims.filter(status='C').count()

    # Count policies of different types
    total_health = policies.filter(type='health').count()
    total_life = policies.filter(type='life').count()
    total_auto = policies.filter(type='auto').count()

    return render(request, 'user_app/main.html', {
        'user': fnuser,
        'total_accepted': total_accepted,
        'total_rejected': total_rejected,
        'total_pending': total_pending,
        'total_health': total_health,
        'total_life': total_life,
        'total_auto': total_auto
    })
    

@login_required
def create_policy(request):
    fnuser = request.user.first_name
    # By default, assume edit mode is False
    edit_mode = False
    
    if request.user.is_staff:
        print("staff if")
        # Admin users will see the full form with the option to edit existing policies
        if request.method == 'POST':
            print("admin post if")
            policy_number = request.POST.get('policy_number')
            if policy_number:
                policy = get_object_or_404(Policy, policy_number=policy_number)
                form = PolicyForm(request.POST, instance=policy)
                edit_mode = True
            else:
                form = PolicyForm(request.POST)
                if form.is_valid():
                    policy = form.save(commit=False)
                    policy.user = request.user
                    policy.save()
                    return redirect('read_policy')
        else:
            policy_number = request.GET.get('policy_number')
            if policy_number:
                policy = get_object_or_404(Policy, policy_number=policy_number)
                form = PolicyForm(instance=policy)
                edit_mode = True
            else:
                form = PolicyForm()
    else:
        print("user else")
        # Normal users will see a simplified form without a policy number field
        if request.method == 'POST':
            print("post if")
            form = PolicyForm(request.POST)
            if form.is_valid():
                policy = form.save(commit=False)
                policy.user = request.user
                policy.save()
                return redirect('read_policy')
        else:
            print("policyform else")
            form = PolicyForm()
            print(form)

    return render(request, 'user_app/create_policy.html', {'form': form, 'edit_mode': edit_mode,'user':fnuser})


@login_required
def read_policy(request):
    # Determine if the user is an admin
    is_admin = request.user.is_staff
    fnuser = request.user.first_name

    if is_admin:
        policies = Policy.objects.all()  # Admin sees all policies
    else:
        policies = Policy.objects.filter(user=request.user)  # Normal user sees their own policies

    if request.method == 'POST' and is_admin:
        action = request.POST.get('action')
        if action == 'verify':
            policy_number = request.POST.get('policy_number')
            policy = get_object_or_404(Policy, policy_number=policy_number)
            policy.verification = True
            policy.save()
        elif action == 'edit':
            policy_number = request.POST.get('policy_number')
            policy = get_object_or_404(Policy, policy_number=policy_number)
            if request.method == 'POST':
                form = PolicyForm(request.POST, instance=policy)
                if form.is_valid():
                    form.save()
                    return redirect('read_policy')
            else:
                form = PolicyForm(instance=policy)
            return render(request, 'user_app/create_policy.html', {'form': form, 'user': fnuser, 'edit_mode': True})
        elif action == 'delete':
            policy_number = request.POST.get('policy_number')
            policy = get_object_or_404(Policy, policy_number=policy_number)
            policy.delete()
            return redirect('read_policy')

    return render(request, 'user_app/read_policy.html', {'policies': policies, 'user': fnuser, 'is_admin': is_admin})


@login_required
def read_claim(request):
    # Determine if the user is an admin
    is_admin = request.user.is_staff
    fnuser = request.user.first_name

    if is_admin:
        claims = Claim.objects.all()  # Admin sees all claims
    else:
        claims = Claim.objects.filter(user=request.user)  # Normal user sees their own claims

    if request.method == 'POST' and is_admin:
        claim_id = request.POST.get('claim_id')
        action = request.POST.get('action')
        
        # Retrieve the claim object
        claim = get_object_or_404(Claim, claim_id=claim_id)
        
        # Update the claim status based on the action
        if action == 'accept':
            claim.status = 'A'
        elif action == 'reject':
            claim.status = 'B'
        
        # Save the updated claim
        claim.save()
        
        # Redirect back to the read_claim view
        return redirect('read_claim')

    return render(request, 'user_app/read_claim.html', {'claims': claims, 'user': fnuser})  


@login_required
def create_claim(request):
    if request.method == 'POST':
        form = ClaimForm(request.user, request.POST)
        fnuser = request.user.first_name
        if form.is_valid():
            claim = form.save(commit=False)
            policy = Policy.objects.get(policy_number=claim.policy_number)
            if policy.is_verified():
                if claim.amt > policy.lumpsum:
                    form.add_error('amt', "Can't claim more than lumpsum")
                    return render(request, 'user_app/create_claim.html', {'form': form, 'user': fnuser, 'policy_not_verified': False})
                claim.user = request.user
                claim.save()
                return redirect('read_claim')
            else:
                return render(request, 'user_app/create_claim.html', {'form': form, 'user': fnuser, 'policy_not_verified': True})
    else:
        form = ClaimForm(request.user)
        fnuser = request.user.first_name

    return render(request, 'user_app/create_claim.html', {'form': form, 'user': fnuser, 'policy_not_verified': False})
    