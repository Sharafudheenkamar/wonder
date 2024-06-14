from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.views import View
import json
from clientapp.forms import *
from clientapp.models import *
from .models import *
from user.models import Userprofile
from django.db.models import Q
from clientapp.models import Client
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse

# Create your views here.
class Adminhomeload(View):
    def get(self, request):
        return render(request, 'adminhome.html')

class Clienthomeload(View):
    def get(self, request):
        user_id = request.session['user_id']
        print(user_id)
        user_profile = Userprofile.objects.filter(id=user_id).first()
        print(user_profile)
        profile_instance = Client.objects.filter(is_active=True, user=user_profile).first()
        visited_places = placevisited.objects.filter(user__id=user_id, is_active=True).all().order_by('-id')
        # myconnectionslistlimit = Connections.objects.filter(user_id=user_id, is_active=True).order_by('-id')[:10]
        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user_id) | Q(clientuserid_id=user_id),is_active=True).order_by('-id')[:10]
        print("myconnectionslistlimit")
        print(myconnectionslistlimit)
        myconnectionslist = Connections.objects.filter(user__id=user_id, is_active=True).all().order_by('-id')
        allgroups = Wandergroup.objects.filter(is_active=True).all()
        connected_client_ids = Connections.objects.filter(user=user_profile, is_active=True).values_list('client_id', flat=True)
        allclients = Client.objects.filter(is_active=True).exclude(user=user_profile).exclude(id__in=connected_client_ids)
        allpost = posts.objects.filter(is_active=True)
        mygroups = Wandergroup.objects.filter(user__id=user_id, is_active=True).all().order_by('-id')
        mygroups2 = Assignedgroups.objects.filter(user__id=user_id, is_active=True).all().order_by('-id')
        mygroups3 = Wandergroup.objects.filter(user=user_profile, is_active=True).all().order_by('-id')
        print("mygroup3")

        created_groups = Wandergroup.objects.filter(user=user_id, is_active=True)

        # Get groups where the user is a member
        member_groups = Wandergroup.objects.filter(assignedgroups__user=user_id, is_active=True)

        # Combine both querysets
        all_groups = Wandergroup.objects.filter(
            Q(user=user_profile) | Q(assignedgroups__user=user_profile),
            is_active=True
        ).distinct()
        print(all_groups)


        print(mygroups3)
        # Create a dictionary to track likes by the current user
        user_likes = Likepost.objects.filter(user=user_profile, postid__in=allpost).values_list('postid', flat=True)
        user_likes_dict = {post_id: True for post_id in user_likes}
        post_data = []
        for post in allpost:
            post_hashtags = hashtag.objects.filter(post=post).values_list('hashtag', flat=True)
            # Join hashtags into a single string with '#' in front of each tag
            hashtags_string = ' '.join(['#' + tag for tag in post_hashtags])
            print('hashtags_string', hashtags_string)
            client_image_url = post.user.client.image.url if post.user.client and post.user.client.image else None
            comments = Commentpost.objects.filter(postid=post, is_active=True).order_by('created_at')
            post_data.append({
                'hashtags_string': hashtags_string,
                'post': post,
                'client_image_url': client_image_url,
                'comments': comments
            })

        context = {

            'profile_instances': user_profile,
            'visited_places': visited_places,
            'myconnectionslist': myconnectionslist,
            'mygroups': mygroups,
            'mygroups2': mygroups2,
            'mygroup3':mygroups3,
            'allgroups': allgroups,
            'allclients': allclients,
            'allpost': post_data,
            'myconnectionslistlimit': myconnectionslistlimit,
            'user_likes_dict': user_likes_dict,
            'all_groups':all_groups,
            'user_id':user_id,
        }

        return render(request, 'index.html', context)
# return render(request, 'cilenthome.html')
class UserLogin(View):
    template_name ="login.html"
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user_type = ""
        response_dict = {"success": False}
        landing_page_url = {
                                    "ADMIN": "loadadmin",
                                   "CLIENT":"loadclient",
                               }

        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        print(password)
        authenticated = authenticate(username=username, password=password)
        try:
            user = Userprofile.objects.get(username=username)

        except Userprofile.DoesNotExist:
            response_dict[
                            "reason"
                        ] = "No account found for this username. Please signup."
            messages.error(request, response_dict["reason"])
        if not authenticated:
            response_dict["reason"] = "Invalid credentials."
            messages.error(request, response_dict["reason"])
            print(response_dict["reason"])
            return render(request, self.template_name, {"response_dict": response_dict})

            # return redirect(request.GET.get("from") or "/user/userlogin")

        else:

            session_dict = {"real_user": authenticated.id}
            token, c = Token.objects.get_or_create(
                        user=user, defaults={"session_dict": json.dumps(session_dict)}
                        )

            user_type = authenticated.user_type

            request.session["data"] = {
                            "user_id": user.id,
                            "user_type": user.user_type,
                            "token": token.key,
                            "username": user.username,
                            "status": user.is_active,
                        }
            print("hai")
            print(user)
            print(user_type)
            request.session["user"] = authenticated.username
            request.session["user_id"] = user.id
            request.session["token"] = token.key
            request.session["status"] = user.is_active
            return redirect(landing_page_url[user_type])
        return redirect(request.GET.get("from") or loadlogin)
class UserLogout(View):
    def get(self,request):
        return redirect('')

# class ForgotPassword(View):
#     def get(self,request):
#         return render(request,'forgot password.html')
#     def post(self, request):
#         email = request.POST.get('email')
#         print('email',email)
#
#         try:
#             clientinstance = Client.objects.filter(email=email).first()
#             print('clientinstance',clientinstance)
#         except Client.DoesNotExist:
#             messages.error(request, 'User not found.')
#             return HttpResponse('User not found.', status=404)
#
#         # Generate OTP
#         otp = get_random_string(length=6, allowed_chars='0123456789')
#         hashedpass=make_password(otp)
#         print(otp)
#         # Save OTP to user model (you may need to add a field for this)
#         clientinstance.user.password = hashedpass
#         clientinstance.user.save()
#
#         # Send OTP through email
#         send_mail(
#             'Forgot Password OTP',
#             f'WanderConnect one time password is : {otp}',
#             'from@example.com',
#             [email],
#             fail_silently=False,
#         )
#
#         # messages.success(request, 'OTP sent successfully.')
#         return HttpResponse('''<script>alert('otp send successfully to your email');window.location='/user/userlogin/'</script>''')
#

from django.http import JsonResponse


class ForgotPassword(View):
    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        print('email', email)

        try:
            clientinstance = Client.objects.filter(email=email,user__username=username).first()
            print('clientinstance', clientinstance)
            if not clientinstance:
                raise Client.DoesNotExist
        except Client.DoesNotExist:
            return JsonResponse({'message': 'User not found.'}, status=404)

        # Generate OTP
        otp = get_random_string(length=6, allowed_chars='0123456789')
        hashedpass = make_password(otp)
        print(otp)

        # Save OTP to user model (you may need to add a field for this)
        clientinstance.user.password = hashedpass
        clientinstance.user.save()

        # Send OTP through email
        send_mail(
            'Forgot Password OTP',
            f'WanderConnect one time password is : {otp}',
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return JsonResponse({'message': 'OTP sent successfully. Check your email.'}, status=200)

