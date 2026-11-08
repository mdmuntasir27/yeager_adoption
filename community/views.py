from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.db.models import Q
from .models import AdoptionPost, AdoptionInquiry
from .forms import AdoptionPostForm, AdoptionInquiryForm, InquiryStatusForm


def post_list(request):
    posts = AdoptionPost.objects.select_related('author', 'author__profile').prefetch_related('adoption_inquiries')

    query = request.GET.get('q', '')
    animal_type = request.GET.get('animal_type', '')
    gender = request.GET.get('gender', '')
    location = request.GET.get('location', '')
    status = request.GET.get('status', 'Open')

    if query:
        posts = posts.filter(
            Q(pet_name__icontains=query) |
            Q(breed__icontains=query) |
            Q(animal_type__icontains=query) |
            Q(description__icontains=query)
        )
    if animal_type:
        posts = posts.filter(animal_type=animal_type)
    if gender:
        posts = posts.filter(gender=gender)
    if location:
        posts = posts.filter(location__icontains=location)
    if status:
        posts = posts.filter(status=status)

    from django.core.paginator import Paginator
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'animal_type': animal_type,
        'gender': gender,
        'location': location,
        'status': status,
        'animal_type_choices': AdoptionPost.ANIMAL_TYPE_CHOICES,
        'gender_choices': AdoptionPost.GENDER_CHOICES,
        'status_choices': AdoptionPost.STATUS_CHOICES,
    }
    return render(request, 'community/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(AdoptionPost, pk=pk)
    already_inquired = False
    user_inquiry = None

    if request.user.is_authenticated:
        user_inquiry = AdoptionInquiry.objects.filter(post=post, requester=request.user).first()
        already_inquired = user_inquiry is not None

    context = {
        'post': post,
        'already_inquired': already_inquired,
        'user_inquiry': user_inquiry,
    }
    return render(request, 'community/post_detail.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = AdoptionPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, f'Your post for {post.pet_name} has been published!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = AdoptionPostForm()
    return render(request, 'community/post_form.html', {'form': form, 'action': 'Create'})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(AdoptionPost, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You can only edit your own posts.')
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        form = AdoptionPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('post_detail', pk=pk)
    else:
        form = AdoptionPostForm(instance=post)
    return render(request, 'community/post_form.html', {'form': form, 'action': 'Edit', 'post': post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(AdoptionPost, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You can only delete your own posts.')
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        pet_name = post.pet_name
        post.delete()
        messages.success(request, f'Post for {pet_name} has been deleted.')
        return redirect('my_posts')
    return render(request, 'community/post_confirm_delete.html', {'post': post})


@login_required
def mark_given(request, pk):
    post = get_object_or_404(AdoptionPost, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You can only update your own posts.')
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        post.status = 'Given'
        post.save()
        messages.success(request, f'{post.pet_name} has been marked as given for adoption.')
    return redirect('post_detail', pk=pk)


@login_required
def submit_inquiry(request, pk):
    post = get_object_or_404(AdoptionPost, pk=pk)

    if post.author == request.user:
        messages.error(request, 'You cannot request to adopt your own pet post.')
        return redirect('post_detail', pk=pk)

    if not post.is_open:
        messages.error(request, 'This pet has already been given for adoption.')
        return redirect('post_detail', pk=pk)

    if AdoptionInquiry.objects.filter(post=post, requester=request.user).exists():
        messages.warning(request, 'You have already sent a request for this pet.')
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        form = AdoptionInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.post = post
            inquiry.requester = request.user
            # Pre-fill phone from user profile if available
            if not inquiry.contact_phone:
                try:
                    inquiry.contact_phone = request.user.profile.phone
                except Exception:
                    pass
            inquiry.save()
            messages.success(request, f'Your adoption request for {post.pet_name} has been sent to {post.author.username}!')
            return redirect('post_detail', pk=pk)
    else:
        initial = {}
        try:
            initial['contact_phone'] = request.user.profile.phone
        except Exception:
            pass
        form = AdoptionInquiryForm(initial=initial)

    return render(request, 'community/inquiry_form.html', {'form': form, 'post': post})


@login_required
def my_posts(request):
    posts = AdoptionPost.objects.filter(author=request.user).prefetch_related('adoption_inquiries')
    return render(request, 'community/my_posts.html', {'posts': posts})


@login_required
def post_inquiries(request, pk):
    post = get_object_or_404(AdoptionPost, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You can only view inquiries for your own posts.')
        return redirect('post_detail', pk=pk)

    inquiries = post.adoption_inquiries.select_related('requester', 'requester__profile')
    return render(request, 'community/post_inquiries.html', {'post': post, 'inquiries': inquiries})


@login_required
def update_inquiry_status(request, inquiry_pk):
    inquiry = get_object_or_404(AdoptionInquiry, pk=inquiry_pk)
    if inquiry.post.author != request.user:
        messages.error(request, 'Permission denied.')
        return redirect('community_home')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Contacted', 'Rejected']:
            inquiry.status = new_status
            inquiry.save()
            messages.success(request, f'Request status updated to {new_status}.')
    return redirect('post_inquiries', pk=inquiry.post.pk)


@login_required
def my_inquiries(request):
    inquiries = AdoptionInquiry.objects.filter(requester=request.user).select_related('post', 'post__author', 'post__author__profile')
    return render(request, 'community/my_inquiries.html', {'inquiries': inquiries})


def public_profile(request, username):
    from django.contrib.auth.models import User
    profile_user = get_object_or_404(User, username=username)
    posts = AdoptionPost.objects.filter(author=profile_user, status='Open')
    context = {
        'profile_user': profile_user,
        'posts': posts,
    }
    return render(request, 'community/public_profile.html', context)
