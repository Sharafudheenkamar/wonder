from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from .models import *
from user.models import Userprofile
from django.contrib.auth.hashers import make_password
import re
from django.db.models import Q
from itertools import chain
class ViewMyVisitedPlace(View):
    def get(self, request):
        user = request.session['user_id']
        visited_places = placevisited.objects.filter(user__id=user, is_active=True).all().order_by('-id')
        print(visited_places)
        return render(request, 'placevisited.html', {'visited_places': visited_places})

class loadaddplacevisited(View):
    def post(self, request):

        form = addplaceform(request.POST)
        if form.is_valid():

            place = form.save(commit=False)
            user = request.session['user_id']
            print(user)
            user1=Userprofile.objects.filter(id=user).first()
            place.user = user1  # Assuming you are using request.user to get the current user
            place.save()
            form = addplaceform()  # Reset the form after saving
        return redirect('viewmyprofile')

class changepassword(View):
    def post(self, request):
        user = request.session['user_id']
        user1=Userprofile.objects.filter(id=user).first()
        hashpass=make_password(request.POST['password'])
        user1.password=hashpass
        user1.save()
        return redirect('viewmyprofile')



class editmyprofile(View):
    def post(self, request,id):
        client = Client.objects.filter(id=id).first()
        form = ClientRegistrationForm1(request.POST,instance=client)
        if form.is_valid():
            editreg = form.save(commit=False)
            user = request.session['user_id']
            print(user)
            user1=Userprofile.objects.filter(id=user).first()
            user1.first_name= request.POST['first_name']
            user1.second_name=request.POST['second_name']
            user1.username=request.POST['username']# Assuming you are using request.user to get the current user
            user1.save()
            editreg.save()
            form = addplaceform()  # Reset the form after saving
        return redirect('viewmyprofile')












class ClientRegistrationView(View):
    def get(self, request):
        form = ClientRegistrationForm()
        return render(request, 'register.html', {'form': form})
    def post(self, request):
        form = ClientRegistrationForm(request.POST, request.FILES)
        print(request.POST['password'])



        # hashpass=make_password()
        if form.is_valid():
            client = form.save(commit=False)
            user = Userprofile.objects.create_user(user_type='CLIENT', username=request.POST['username'],
                                            password=request.POST['password'], first_name=request.POST['first_name'],second_name=request.POST['second_name'],)
            client.user = user
            client.save()
            return redirect('userlogin')
        return render(request, 'register.html', {'form': form})


#
# class changeimage(View):
#     def post(self,request):
#         user = request.session['user_id']
#         user1 = Userprofile.objects.filter(id=user).first()
#         profile_instances = Client.objects.filter(is_active=True, user=user1).first()
#         user.image=request.POST['image']

class changeimage(View):
    def post(self, request):
        user_id = request.session['user_id']
        user_profile = Userprofile.objects.filter(id=user_id).first()
        client_profile = Client.objects.filter(is_active=True, user=user_profile).first()
        print(client_profile.image)
        image_file = request.FILES.get('image1')
        print("hhhhhh",image_file)
        if image_file:
            # If an image was uploaded
            client_profile.image = image_file
            client_profile.save()
        return redirect('viewmyprofile')

    # class geteditvisitedplace(View):
#     def get(self,request,data):
#         list = placevisited.objects.filter(is_active=True).first()
#         return render(request,'editvisitedplaces.html',{'form':list})
#     def post(self,request,data):
#         listinstance = placevisited.objects.filter(id=data, is_active=True).first()
#         form=addplaceform(request.POST,request.FILES,instance=listinstance)
#         if form.is_valid():
#             form.save()
#             return redirect('viewmyvisitedplace')
# class deletevistedplaces(View):
#     def get(self,request,data):
#         place_instances = placevisited.objects.filter(is_active=True,id=data).first()
#         return render(request,'deletevistedplace.html',{'place_instance':place_instances})
#     def post(self,request,data):
#         place_instances=placevisited.objects.filter(is_active=True,id=data).first()
#         place_instances.is_active=False
#         place_instances.save()
#         return redirect('viewmyvisitedplace')

class viewmyprofile(View):
    def get(self,request):
        user = request.session['user_id']
        print(user)
        user1 = Userprofile.objects.filter(id=user).first()
        print(user1)
        profile_instances = Client.objects.filter(is_active=True,user=user1).first()
        visited_places = placevisited.objects.filter(user__id=user, is_active=True).all().order_by('-id')
        myconnectionslist=Connections.objects.filter(user__id=user, is_active=True).all().order_by('-id')
        mygroups=Wandergroup.objects.filter(user__id=user, is_active=True).all().order_by('-id')
        mygroups2 =Assignedgroups.objects.filter(user__id=user, is_active=True).all().order_by('-id')
        return render(request,'profile.html',{'profile_instances':profile_instances,'visited_places':visited_places,'myconnectionslist':myconnectionslist,'mygroups':mygroups,'mygroups2':mygroups2})

class loadaddpost(View):
    def get(self, request):
        form = addpostform()
        user = request.session['user_id']
        print(user)
        user1 = Userprofile.objects.filter(id=user).first()
        print(user1)
        profile_instances1 = Client.objects.filter(is_active=True, user=user1).first()
        print("ppp")
        print(profile_instances1)
        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                            is_active=True).order_by('-id')[:10]

        created_groups = Wandergroup.objects.filter(user=user, is_active=True)

        # Get groups where the user is a member
        member_groups = Wandergroup.objects.filter( assignedgroups__is_active=True,assignedgroups__user=user, is_active=True)

        # Combine both querysets
        all_groups = created_groups | member_groups

        return render(request,'createpost.html', {'form': form,'profile_instances1':profile_instances1,'profile_instances':user1,'myconnectionslistlimit':myconnectionslistlimit,'all_groups':all_groups})

    def post(self, request):
        print("addd post")
        form = addpostform(request.POST,request.FILES)
        if form.is_valid():
            posts = form.save(commit=False)
            user = request.session['user_id']
            print(user)
            user1=Userprofile.objects.filter(id=user).first()
            posts.user = user1  # Assuming you are using request.user to get the current user
            posts.save()
            import re
            # Input string
            input_string = request.POST.get("hash_tag")
            print(input_string)
            # Regular expression pattern to match hash tags, remove spaces, and remove other characters

            input_string = request.POST.get("hash_tag")
            pattern = r'#\w+'
            hashtags_with_symbol = re.findall(pattern, input_string)

            # Remove '#' and spaces from each hashtag
            tags = [tag.replace("#", "").strip() for tag in hashtags_with_symbol]

            print(tags)
            for tag in tags:
                hashtag1 = hashtag.objects.create(user=user1, post=posts, hashtag=tag)
                hashtag1.save()
            form = addpostform()  # Reset the form after saving
        # return render(request, 'createpost.html', {'form': form})
        return redirect('viewmypost')
class viewmypost(View):
    def get(self,request):
        user = request.session['user_id']
        print(user)
        user1 = Userprofile.objects.filter(id=user).first()
        post_list = posts.objects.filter(user=user1, is_active=True).all()
        profile_instances = Client.objects.filter(is_active=True, user=user).first()
        profile_instanceuser = Userprofile.objects.filter(is_active=True, id=user).first()
        print("profile_instances")
        print(profile_instances)
        print(profile_instanceuser)
        print(post_list)
        user_likes = Likepost.objects.filter(user=user1, postid__in=post_list).values_list('postid', flat=True)
        user_likes_dict = {post_id: True for post_id in user_likes}
        post_data = []
        ordered_post_list = post_list.order_by('-created_at')
        for post in ordered_post_list:
            print('post',post)
            post_hashtags = hashtag.objects.filter(post=post).values_list('hashtag', flat=True)
            # Join hashtags into a single string with '#' in front of each tag
            hashtags_string = ' '.join(['#' + tag for tag in post_hashtags])
            print('hashtags_string',hashtags_string)
            client_image_url = post.user.client.image.url if post.user.client and post.user.client.image else None
            comments = Commentpost.objects.filter(postid=post, is_active=True).order_by('created_at')
            post_data.append({
                'hashtags_string':hashtags_string,
                'post': post,
                'client_image_url': client_image_url,
                'comments': comments
            })
        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                            is_active=True).order_by('-id')[:10]
        print("postconnectionlimit")
        print(myconnectionslistlimit)

        created_groups = Wandergroup.objects.filter(user=user, is_active=True)

        # Get groups where the user is a member
        member_groups = Wandergroup.objects.filter( assignedgroups__is_active=True,assignedgroups__user=user, is_active=True)

        # Combine both querysets
        all_groups = Wandergroup.objects.filter(
            Q(user=user) | Q(assignedgroups__user=user),
            is_active=True
        ).distinct()
        return render(request, 'viewmypost.html',{

            'profile_instances': profile_instanceuser,
            'profile_instances1': profile_instances,

            'posts_with_hashtags': post_data,

            'user_likes_dict': user_likes_dict,

            'myconnectionslistlimit':myconnectionslistlimit,

              'user_id':user,
            'all_groups':all_groups,
                                                  })




#client#views.py
import uuid
class Addwandergroup(View):
    def get(self,request):
        user = request.session['user_id']
        print(user)
        profile_instances = Userprofile.objects.filter(id=user).first()
        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                            is_active=True).order_by('-id')[:10]
        print("postconnectionlimit")
        print(myconnectionslistlimit)

        created_groups = Wandergroup.objects.filter(user=user, is_active=True)

        # Get groups where the user is a member
        member_groups = Wandergroup.objects.filter( assignedgroups__is_active=True,assignedgroups__user=user, is_active=True)


        # Combine both querysets
        all_groups = created_groups | member_groups
        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                       is_active=True).order_by('-id')[:10]
        return render(request,'creategroup.html',{'user_id':user,'profile_instances':profile_instances,'all_groups':all_groups,'myconnectionslistlimit':myconnectionslistlimit,'myconnectionslistlimit':myconnectionslistlimit})

    def post(self, request):
        user_id = request.session.get('user_id')
        if user_id is None:
            return HttpResponse("User ID not found in session")

        user = Userprofile.objects.filter(is_active=True, id=user_id).first()
        profile_instances = Userprofile.objects.filter(is_active=True, id=user_id).first()
        created_groups = Wandergroup.objects.filter(user=user, is_active=True)

        # Get groups where the user is a member
        member_groups = Wandergroup.objects.filter( assignedgroups__is_active=True,assignedgroups__user=user, is_active=True)


        # Combine both querysets
        all_groups = created_groups | member_groups
        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                       is_active=True).order_by('-id')[:10]
        if user is None:
            return HttpResponse("User not found")

        wandergroup_instances = Wandergroup.objects.filter(is_active=True, user=user)
        form = Addwandergroupform(request.POST, request.FILES)
        if form.is_valid():
            new_wandergroup = form.save(commit=False)
            new_wandergroup.is_active=True
            new_wandergroup.user = user
            new_wandergroup.grouplink = str(uuid.uuid4())  # Generate unique grouplink
            input_string = request.POST.get("hash_tag")
            print(input_string)
            # Regular expression pattern to match hash tags, remove spaces, and remove other characters

            input_string = request.POST.get("hash_tag")
            pattern = r'#\w+'
            hashtags_with_symbol = re.findall(pattern, input_string)

            # Remove '#' and spaces from each hashtag
            tags = [tag.replace("#", "").strip() for tag in hashtags_with_symbol]


            new_wandergroup.grouplink = new_wandergroup.get_grouplink()
            print (new_wandergroup)
            new_wandergroup.save()
            Assignedgroups.objects.create(user=user, groupid=new_wandergroup,status=True,is_active=True)

            # Update grouplink for the newly created wandergroup_instance

            # Iterate over each Wandergroup instance and set the grouplink
            for wandergroup_instance in wandergroup_instances:
                wandergroup_instance.grouplink = wandergroup_instance.grouplink
                wandergroup_instance.save()

            print(tags)
            for tag in tags:
                hashtag1 = grouphashtag.objects.create(user=user, group=new_wandergroup, hashtag=tag)
                hashtag1.save()
            # return redirect
            myconnectionslist = Connections.objects.filter(Q(user=user, is_active=True)|Q(clientuserid=user, is_active=True)).all().order_by('-id')

            wandergroup_instances1 = Wandergroup.objects.filter(is_active=True, user=user,id=new_wandergroup.id).first()
            groupmemberinstance=Assignedgroups.objects.filter(is_active=True,groupid=new_wandergroup.id)
            # return render(request, 'createdgroups.html', {'user_id':user,'all_groups':all_groups,'myconnectionslistlimit':myconnectionslistlimit,
            #                                               'profile_instances':profile_instances,'wandergroup_instances': wandergroup_instances1,'groupmemberinstance':groupmemberinstance,
            #                                               'myconnectionslist':myconnectionslist,'profile_instances':profile_instances})
            return render(request, 'createdgroups1.html',
                      {'user_id': user_id, 'all_groups': all_groups, 'myconnectionslistlimit': myconnectionslistlimit,
                       'profile_instances': profile_instances, 'wandergroup_instances': wandergroup_instances1,'new_wandergroup':new_wandergroup,
                       'groupmemberinstance': groupmemberinstance,
                       'myconnectionslist': myconnectionslist, 'profile_instances': profile_instances})

        else:
            return HttpResponse("Form is not valid")
#view my group from myprofile
class Viewwandergroup(View):
    def get(self,request,id):
        user=request.session['user_id']
        user_profile=Userprofile.objects.filter(id=user).first()
        profile_instances = Userprofile.objects.filter(id=user).first()
        print(user)
        created_groups = Wandergroup.objects.filter(user=user, is_active=True)

        # Get groups where the user is a member
        member_groups = Wandergroup.objects.filter( assignedgroups__is_active=True,assignedgroups__user=user, is_active=True)

        # Combine both querysets
        all_groups = Wandergroup.objects.filter(
            Q(user=user) | Q(assignedgroups__user=user),
            is_active=True
        ).distinct()

        myconnectionslist = Connections.objects.filter(Q(user_id=user, is_active=True)|Q(clientuserid_id=user,is_active=True)).all().order_by('-id')
        print('gggggg',myconnectionslist)
        wandergroup_instances1 = Wandergroup.objects.filter(is_active=True, id=id).first()
        groupmemberinstance = Assignedgroups.objects.filter(is_active=True, groupid=id)
        post_instances = posts.objects.filter(groupid__id=id,is_active=True).all()
        post_data = []
        for post in post_instances:
            client_image_url = post.user.client.image.url if post.user.client and post.user.client.image else None
            comments = Commentpost.objects.filter(postid=post, is_active=True).order_by('created_at')
            post_data.append({
                'post': post,
                'client_image_url': client_image_url,
                'comments': comments
            })
        user_likes = Likepost.objects.filter(user=user_profile, postid__in=post_instances).values_list('postid', flat=True)
        user_likes_dict = {post_id: True for post_id in user_likes}
        print('post_instances',post_instances)
        print(groupmemberinstance)
        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                       is_active=True).order_by('-id')[:10]
        return render(request, 'createdgroups.html',{'profile_instances':profile_instances,'user_id':user,'all_groups':all_groups,'user_id':user,'wandergroup_instances': wandergroup_instances1,'myconnectionslistlimit':myconnectionslistlimit, 'groupmemberinstance': groupmemberinstance,'myconnectionslist':myconnectionslist,'post_instances':post_data,'user_likes_dict':user_likes_dict,'profile_instances':profile_instances})
class Viewwandergroup1(View):
    def get(self,request,id):
        user=request.session['user_id']
        user_profile=Userprofile.objects.filter(id=user).first()
        profile_instances = Userprofile.objects.filter(id=user).first()
        print(user)
        created_groups = Wandergroup.objects.filter(user=user, is_active=True)

        # Get groups where the user is a member
        member_groups = Wandergroup.objects.filter( assignedgroups__is_active=True,assignedgroups__user=user, is_active=True)

        # Combine both querysets
        all_groups = created_groups | member_groups

        myconnectionslist = Connections.objects.filter(Q(user_id=user, is_active=True)|Q(clientuserid_id=user,is_active=True)).all().order_by('-id')
        print('gggggg',myconnectionslist)
        wandergroup_instances1 = Wandergroup.objects.filter(is_active=True, id=id).first()
        groupmemberinstance = Assignedgroups.objects.filter(is_active=True, groupid=id)
        post_instances = posts.objects.filter(groupid__id=id,is_active=True).all()
        post_data = []
        for post in post_instances:
            client_image_url = post.user.client.image.url if post.user.client and post.user.client.image else None
            comments = Commentpost.objects.filter(postid=post, is_active=True).order_by('created_at')
            post_data.append({
                'post': post,
                'client_image_url': client_image_url,
                'comments': comments
            })
        user_likes = Likepost.objects.filter(user=user_profile, postid__in=post_instances).values_list('postid', flat=True)
        user_likes_dict = {post_id: True for post_id in user_likes}
        print('post_instances',post_instances)
        print(groupmemberinstance)
        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                       is_active=True).order_by('-id')[:10]
        return render(request, 'createdgroups3.html',{'profile_instances':profile_instances,'user_id':user,'all_groups':all_groups,'user_id':user,'wandergroup_instances': wandergroup_instances1,'myconnectionslistlimit':myconnectionslistlimit, 'groupmemberinstance': groupmemberinstance,'myconnectionslist':myconnectionslist,'post_instances':post_data,'user_likes_dict':user_likes_dict,'profile_instances':profile_instances})



class Editewandergroup(View):
    def get(self,request,id):
        user=request.session['user_id']
        user_profile=Userprofile.objects.filter(id=user).first()
        profile_instances = Userprofile.objects.filter(id=user).first()
        wandergroup_instances = Wandergroup.objects.filter(is_active=True,id=id).first()
        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                            is_active=True).order_by('-id')[:10]

        return render(request,'client/editwandergroup.html',{'user_id':user,'wandergroup_instance':wandergroup_instances,'myconnectionslistlimit':myconnectionslistlimit})
    def post(self,request,id):
        user=request.session['user_id']
        user_profile=Userprofile.objects.filter(id=user).first()
        profile_instances = Userprofile.objects.filter(id=user).first()
        wandergroup_instances=Wandergroup.objects.filter(is_active=True).all()
        wandergroup_instance = Wandergroup.objects.filter(is_active=True,id=id).first()
        form=Addwandergroupform(request.POST,request.FILES,instance=wandergroup_instance)
        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                            is_active=True).order_by('-id')[:10]

        if form.is_valid():
            form.save()
            return render(request,'client/viewwandergroup.html',{'user_id':user,'wandergroup_instances':wandergroup_instances})
class Deletewandergroup(View):
    # def get(self,request,id):
    #     wandergroup_instances = Wandergroup.objects.filter(is_active=True,id=id).first()
    #     return render(request,'deletewandergroup.html',{'wandergroup_instance':wandergroup_instances})
    def get(self,request,id):
        wandergroup_instances=Wandergroup.objects.filter(is_active=True).all()
        wandergroup_instance = Wandergroup.objects.filter(is_active=True,id=id).first()
        wandergroup_instance.is_active=False
        wandergroup_instance.save()
        user = request.session['user_id']
        profile_instances = Userprofile.objects.filter(id=user).first()
        user_groups = Wandergroup.objects.filter(user=profile_instances)
        mygrouprequest = Assignedgroups.objects.filter(is_active=False, groupid__in=user_groups)

        created_group_ids = Wandergroup.objects.filter(user=user).values_list('id', flat=True)

        member_group_ids = Assignedgroups.objects.filter(user=user).values_list('groupid_id', flat=True)

        # Exclude groups that are either created by the user or where the user is a member
        available_groups = Wandergroup.objects.filter(is_active=True).exclude(
            id__in=created_group_ids.union(member_group_ids))

        created_groups = Wandergroup.objects.filter(user=user, is_active=True)

        # Get groups where the user is a member
        member_groups = Wandergroup.objects.filter( assignedgroups__is_active=True,assignedgroups__user=user, is_active=True)

        # Combine both querysets
        all_groups = created_groups | member_groups

        # Remove duplicates if any (though unlikely with proper ForeignKey relations)
        all_groups = all_groups.distinct()

        myconnectionslist = Connections.objects.filter(user=user, is_active=True).all().order_by('-id')
        wandergroup_instances1 = Wandergroup.objects.filter(is_active=True).all()

        mygroups = Wandergroup.objects.filter(user__id=user, is_active=True).all().order_by('-id')

        # groupmemberinstance = Assignedgroups.objects.filter(is_active=True, groupid=id)
        # print(groupmemberinstance)

        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                            is_active=True).order_by('-id')[:10]

        return render(request, 'groupview.html',
                      {'profile_instances': profile_instances, 'wandergroup_instances': available_groups,
                       'myconnectionslist': myconnectionslist, 'all_groups': all_groups,
                       'created_groups': created_groups, 'member_groups': member_groups,
                       'myconnectionslistlimit': myconnectionslistlimit, 'mygrouprequest': mygrouprequest})


# return render(request,'viewwandergroup.html',{'wandergroup_instances':wandergroup_instances})
def join_group(request, grouplink):
    try:
        user_id = request.session['user_id']
        user_id = Userprofile.objects.filter(id=user_id, is_active=True).first()
        print('trygroup',grouplink)
        group = Wandergroup.objects.filter(grouplink="/client/join/"+grouplink).first()
        print(group)
        Assignedgroups.objects.create(user=user_id,groupid=group,status=True)
        group_instances=Assignedgroups.objects.filter(user=user_id,is_active=True,status=True).all()
        print(group_instances)
        # Add logic to handle joining the group
        # For example, you might add the user to the group
        return render(request, 'client/membergroups.html', {'group_instances': group_instances})
    except Wandergroup.DoesNotExist:
        return render(request, 'join_group_error.html')
def join_group2(request, grouplink):
    try:
        user_id = request.session['user_id']
        user_id = Userprofile.objects.filter(id=user_id, is_active=True).first()
        print('trygroup',grouplink)
        group = Wandergroup.objects.filter(grouplink="/client/join/"+grouplink).first()
        print(group)
        Assignedgroups.objects.create(user=user_id,groupid=group,status=False)
        group_instances=Assignedgroups.objects.filter(user=user_id,is_active=True,status=True).all()
        print(group_instances)
        # Add logic to handle joining the group
        # For example, you might add the user to the group
        return render(request, 'client/membergroups.html', {'group_instances': group_instances})
    except Wandergroup.DoesNotExist:
        return render(request, 'join_group_error.html')
from clientapp.models import Client
class Sharelink(View):
    def get(self,request,id):
        user_id = request.session['user_id']
        user_id = Userprofile.objects.filter(id=user_id, is_active=True).first()

        wandergroup_instance=Wandergroup.objects.filter(id=id).first()
        user_instances = Client.objects.exclude(user=user_id)
        return render(request,'client/sharelink.html',{'user_instances':user_instances,'wandergroup_instance':wandergroup_instance})

    def post(self, request):
        client_ids = request.POST.getlist('clients')
        print(client_ids)
        grouplink=request.POST['grouplink']
        groupid=request.POST['groupid']
        groupid=Wandergroup.objects.filter(id=groupid).first()
        user_id=request.session['user_id']
        user_id=Userprofile.objects.filter(id=user_id,is_active=True).first()
        # Assuming 'user_instances' is the queryset of Userprofile instances
        for client_id in client_ids:
            clid=Client.objects.filter(id=client_id).first()
            Groupinvitation.objects.create(user=user_id, toid_id=clid.user.id, i_type='sharelink',grouplink=grouplink,
                                                   group=groupid,status=False)
        return redirect('invitation_sent')  #
class Invitelink(View):
    def get(self, request, id):
        user_id = request.session['user_id']
        user_id = Userprofile.objects.filter(id=user_id, is_active=True).first()

        wandergroup_instance = Wandergroup.objects.filter(id=id).first()
        user_instances = Connections.objects.filter(user=user_id).all()
        return render(request, 'client/invitelink.html',
                      {'user_instances': user_instances, 'wandergroup_instance': wandergroup_instance})

    def post(self, request):
        client_ids = request.POST.getlist('clients')
        print(client_ids)
        grouplink = request.POST['grouplink']
        groupid=request.POST['groupid']
        groupid=Wandergroup.objects.filter(id=groupid).first()
        user_id = request.session['user_id']
        user_id = Userprofile.objects.filter(id=user_id, is_active=True).first()
        # Assuming 'user_instances' is the queryset of Userprofile instances
        for client_id in client_ids:
            clid = Client.objects.filter(id=client_id).first()
            Groupinvitation.objects.create(user=user_id, toid_id=clid.user.id, i_type='invitation', grouplink=grouplink,group=groupid,status=True)
        return redirect('invitation_sent')
class Addconnections(View):
    def get(self,request):

        user_id = request.session['user_id']
        user_id = Userprofile.objects.filter(id=user_id, is_active=True).first()
        connected_client_ids = Connections.objects.filter(Q(user__id=request.session['user_id'],is_active=True)|Q(clientuserid=user_id,is_active=True)).values_list('client_id',
                                                                                                         flat=True)

        # Exclude connected clients from the list of available users
        user_instances = Client.objects.filter(is_active=True).exclude(user=user_id).exclude(
            id__in=connected_client_ids)
        return render(request, 'client/addconnections.html',
                      {'user_instances': user_instances})

    def post(self,request):
        user_id = request.session['user_id']
        user_id = Userprofile.objects.filter(id=user_id, is_active=True).first()
        clientid=Client.objects.filter(id=request.POST['client'],is_active=True).first()
        print(clientid)
        clientuserid=Userprofile.objects.filter(id=request.POST['clientuserid'],is_active=True).first()
        print(clientuserid)
        Connections.objects.create(user=user_id,client=clientid,clientuserid=clientuserid,is_active=False)
        connection_instances=Connections.objects.filter(Q(user__id=request.session['user_id'],is_active=True)|Q(clientuserid=user_id,is_active=True)).all()
        # return redirect('viewmyprofile')
        return redirect('viewmyconnections1')

class Viewconnections(View):
    def get(self,request):

        user_id = request.session['user_id']
        user_id = Userprofile.objects.filter(id=user_id, is_active=True).first()

        # wandergroup_instance = Wandergroup.objects.filter(id=id).first()
        connection_instances = Connections.objects.filter(Q(user__id=request.session['user_id'],is_active=True)|Q(clientuserid=user_id,is_active=True)).all()
        return render(request, 'client/viewconnections.html',{'connection_instances': connection_instances})
    def post(self,request,id):
        connection_instances = Connections.objects.filter(id=id).first()
        print(connection_instances)
        connection_instances.delete()

        user_id = request.session['user_id']
        user_id = Userprofile.objects.filter(id=user_id, is_active=True).first()
        # Connections.objects.create(user=user_id,client__id=request.POST[client],clientuserid=request.POST['clientuserid'])
        connection_instances=Connections.objects.filter(Q(user__id=request.session['user_id'],is_active=True)|Q(clientuserid=user_id,is_active=True)).all()
        return render(request,'client/viewconnections.html',{'connection_instances':connection_instances})

#
# class Viewmembergroups(View):
#     group_instances=Assignedgroups()
import socket
class Viewinvitations(View):
    def get(self,request):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        user_id = request.session['user_id']
        user_id = Userprofile.objects.filter(id=user_id, is_active=True).first()
        invitation_instances=Groupinvitation.objects.filter(toid=user_id,i_type='invitation').all()
        print(invitation_instances)
        return render(request,'client/viewinvitations.html',{'invitation_instances':invitation_instances,'ip_address':ip_address})
class Viewsharelinks(View):
    def get(self,request):
        user_id = request.session['user_id']
        user_id = Userprofile.objects.filter(id=user_id, is_active=True).first()
        print(user_id)
        invitation_instances=Groupinvitation.objects.filter(toid=user_id,i_type='sharelink').all()
        return render(request,'client/viewsharelinks.html',{'invitation_instances':invitation_instances})
class Viewmembergroups(View):
    def get(self,request):
        user_id = request.session['user_id']
        user_id = Userprofile.objects.filter(id=user_id, is_active=True).first()
        print(user_id)
        myconnectionslist=Connections.objects.filter(user__id=user_id, is_active=True).all().order_by('-id')

        assign_instances=Assignedgroups.objects.filter(user=user_id,status=True).all()
        return render(request,'client/membergroups.html',{'assign_instances':assign_instances,'myconnectionslist':myconnectionslist})



class deletepost(View):
    def get(self,request,id):
        postintance = posts.objects.filter(id=id).first()
        if postintance:
            postintance.is_active= False
            postintance.save()
        return redirect('viewmypost')

class editpost(View):
    def get(self, request, id):
        post_instance = posts.objects.filter(id=id).first()
        posts_with_hashtags = []
        # Ensure post_instance is not None before iterating
        if post_instance:
            # Get hashtags related to the post
            post_hashtags = hashtag.objects.filter(post=post_instance).values_list('hashtag', flat=True)
            # Join hashtags into a single string with '#' in front of each tag
            hashtags_string = ' '.join(['#' + tag for tag in post_hashtags])
            # Append the post id, post content, and hashtags to the list
            posts_with_hashtags.append(
                {'post_id': post_instance.id, 'post': post_instance, 'hashtags': hashtags_string})
        print(posts_with_hashtags)
        user = request.session['user_id']
        user1 = Userprofile.objects.filter(id=user).first()
        profile_instances = Client.objects.filter(is_active=True, user=user1).first()
        if posts_with_hashtags:
            return render(request,'editpost.html',{'postintance':post_instance,'hashtags':hashtags_string,'profile_instances':profile_instances})

    def post(self, request, id):
        post_instance = posts.objects.filter(id=id).first()
        if post_instance:
            # Filter and delete all hashtags related to the post
            hashtag.objects.filter(post=post_instance).delete()

            form = addpostform(request.POST, request.FILES, instance=post_instance)
            if form.is_valid():
                post_instance = form.save(commit=False)
                user = request.session.get('user_id')
                user1 = Userprofile.objects.filter(id=user).first() if user else None

                if user1:
                    post_instance.user = user1
                    post_instance.save()

                    input_string = request.POST.get("hash_tag", "")
                    pattern = r'#\w+'
                    hashtags_with_symbol = re.findall(pattern, input_string)

                    # Remove '#' and spaces from each hashtag
                    tags = [tag.replace("#", "").strip() for tag in hashtags_with_symbol]

                    for tag in tags:
                        hashtag1 = hashtag.objects.create(user=user1, post=post_instance, hashtag=tag)
                        hashtag1.save()

                    return redirect('viewmypost')

        # Handle case where the form is not valid or post_instance is None
        form = addpostform(instance=post_instance)
        return render(request, 'editpost.html', {'form': form})

#view my group page
class viewmywandergroup(View):
    def get(self,request):
        user=request.session['user_id']
        profile_instances = Userprofile.objects.filter(id=user).first()
        user_groups = Wandergroup.objects.filter(user=profile_instances)
        mygrouprequest = Assignedgroups.objects.filter(is_active=False, groupid__in=user_groups,groupaddmode='request')

        created_group_ids = Wandergroup.objects.filter(user=user).values_list('id', flat=True)

        member_group_ids = Assignedgroups.objects.filter(user=user).values_list('groupid_id', flat=True)

        # Exclude groups that are either created by the user or where the user is a member
        available_groups = Wandergroup.objects.filter(is_active=True).exclude(id__in=created_group_ids.union(member_group_ids))

        created_groups = Wandergroup.objects.filter(user=user, is_active=True)

        # Get groups where the user is a member
        member_groups = Wandergroup.objects.filter( assignedgroups__is_active=True,assignedgroups__user=profile_instances,is_active=True).exclude(user_id=user)

        # Combine both querysets
        all_groups = created_groups | member_groups

        # Remove duplicates if any (though unlikely with proper ForeignKey relations)
        all_groups = all_groups.distinct()

        myconnectionslist = Connections.objects.filter(user=user, is_active=True).all().order_by('-id')
        wandergroup_instances1 = Wandergroup.objects.filter(is_active=True).all()

        mygroups = Wandergroup.objects.filter(user__id=user, is_active=True).all().order_by('-id')

        # groupmemberinstance = Assignedgroups.objects.filter(is_active=True, groupid=id)
        # print(groupmemberinstance)

        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                            is_active=True).order_by('-id')[:10]




        return render(request, 'groupview.html',{'user_id':user,'profile_instances':profile_instances,'wandergroup_instances': available_groups,'myconnectionslist':myconnectionslist,'all_groups':all_groups,'created_groups':created_groups,'member_groups':member_groups,'myconnectionslistlimit': myconnectionslistlimit,'mygrouprequest':mygrouprequest})

class gropuyoucanjoinindetail(View):
    def get(self, request,id):
        user = request.session['user_id']
        profile_instances=Userprofile.objects.filter(id=user).first()
        wandergroup_instances1 = Wandergroup.objects.filter(is_active=True, id=id).first()
        groupmemberinstance = Assignedgroups.objects.filter(is_active=True, groupid=id)
        groupmember_count = Assignedgroups.objects.filter(is_active=True, groupid=id).count()
        print(groupmember_count)
        postingroup=posts.objects.filter(is_active=True,groupid=id)
        print("group post")
        print(postingroup)
        created_groups = Wandergroup.objects.filter(user=profile_instances, is_active=True)

        # Get groups where the user is a member
        member_groups = Wandergroup.objects.filter( assignedgroups__is_active=True,assignedgroups__user=profile_instances, is_active=True)

        # Combine both querysets
        all_groups = created_groups | member_groups
        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                       is_active=True).order_by('-id')[:10]
        return render(request, 'groupyoucanjoinindetail.html',{'wandergroup_instances': wandergroup_instances1,'groupmemberinstance':groupmemberinstance,'groupmember_count':groupmember_count,'postingroup':postingroup,'profile_instances':profile_instances,'myconnectionslistlimit':myconnectionslistlimit,'all_groups':all_groups})


# class viewmygroup(View):
#     def get(self,request,id):
#         user = request.session['user_id']
#         myconnectionslist = Connections.objects.filter(user=user, is_active=True).all().order_by('-id')
#         wandergroup_instances1 = Wandergroup.objects.filter(is_active=True, user=user,id=id).first()
#         groupmemberinstance=Assignedgroups.objects.filter(is_active=True,groupid=id)
#         return render(request, 'createdgroups.html', {'wandergroup_instances': wandergroup_instances1,'groupmemberinstance':groupmemberinstance,'myconnectionslist':myconnectionslist})


# create group post
class loadaddgrouppost(View):
    def get(self, request,id):
        print("groupid")
        print (id)
        form = addpostform()
        user = request.session['user_id']
        print(user)
        user1 = Userprofile.objects.filter(id=user).first()
        print(user1)
        profile_instances = Client.objects.filter(is_active=True, user=user1).first()

        print(profile_instances)
        return render(request,'creategrouppost.html', {'form': form,'profile_instances':profile_instances,'gid':id})

    def post(self, request):
        print("addd post")
        form = addpostform(request.POST,request.FILES)
        if form.is_valid():
            posts = form.save(commit=False)
            user = request.session['user_id']
            print(user)
            user1=Userprofile.objects.filter(id=user).first()
            group=Wandergroup.objects.filter(id=request.POST.get("gid")).first()
            posts.groupid=group
            posts.user = user1  # Assuming you are using request.user to get the current user
            posts.save()
            import re
            # Input string
            input_string = request.POST.get("hash_tag")
            print(input_string)
            # Regular expression pattern to match hash tags, remove spaces, and remove other characters

            input_string = request.POST.get("hash_tag")
            pattern = r'#\w+'
            hashtags_with_symbol = re.findall(pattern, input_string)

            # Remove '#' and spaces from each hashtag
            tags = [tag.replace("#", "").strip() for tag in hashtags_with_symbol]

            print(tags)
            for tag in tags:
                hashtag1 = hashtag.objects.create(user=user1, post=posts, hashtag=tag)
                hashtag1.save()
            form = addpostform()  # Reset the form after saving
        return render(request, 'creategrouppost.html', {'form': form})

#join request to a group

class joingrouprequest(View):
    def get(self,request,gid):
        user = request.session['user_id']
        user1 = Userprofile.objects.filter(id=user).first()
        group = Wandergroup.objects.filter(id=gid).first()
        # Create a new Assignedgroups instance
        assigned_group = Assignedgroups(user=user1, groupid=group,is_active=False,groupaddmode='request')
        # Save the instance to the database
        assigned_group.save()
        return redirect('viewmywandergroup')
class viewmyconnections1(View):
    def get(self,request):
        user = request.session['user_id']

        print('user',user)
        user1 = Userprofile.objects.filter(id=user).first()
        print('user1',user1)
        # profile_instance = Client.objects.filter(is_active=True, user=user_profile).first()
        profile_instances = Userprofile.objects.filter(id=user).first()
        print("connection profile")
        print(profile_instances)
        print(profile_instances.email)

        simple_query1 = Connections.objects.filter(clientuserid=user1,).all()
        print('simple_query1',simple_query1)
        # Check user field
        simple_query2 = Connections.objects.filter(user=user1).all()
        print('simple_query2',simple_query2)
        connected_client_ids=list(chain(simple_query1, simple_query2))
        print("connected_client_ids")
        print(connected_client_ids)



        for i in connected_client_ids:
            print(i.user)
            print(i.clientuserid)
        connected_user_ids1 = [connection.user.id for connection in connected_client_ids]
        connected_user_ids1.append(user1.id)
        connected_user_ids2 = [connection.clientuserid.id for connection in connected_client_ids]
        combined_user_ids = connected_user_ids1 + connected_user_ids2
        print("connected_user_ids")
        print(connected_user_ids1)
        # profile_instances = Client.objects.filter(is_active=True, user=user1).first()
        # allclients = Client.objects.filter(is_active=True).exclude(user=connected_client_ids.user)
        allclients = Client.objects.filter(is_active=True).exclude(user__id__in=combined_user_ids)
        print("allclients")
        print(allclients)
        # connection_instances = Connections.objects.filter(Q(user__id=request.session['user_id'],is_active=True)|Q(clientuserid=user,is_active=True)).all()
        # myconnectionslist = Connections.objects.filter(user__id=user, is_active=True).all().order_by('-id')
        myconnectionslist=Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),is_active=True).order_by('-id')
        print("myconnectionslist")
        print(myconnectionslist)

        created_groups = Wandergroup.objects.filter(user=user, is_active=True)

        # Get groups where the user is a member
        member_groups = Wandergroup.objects.filter( assignedgroups__is_active=True,assignedgroups__user=user, is_active=True)

        # Combine both querysets
        all_groups = Wandergroup.objects.filter(
            Q(user=user) | Q(assignedgroups__user=user),
            is_active=True
        ).distinct()


        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                       is_active=True).order_by('-id')[:10]
        return render(request, 'viewmyconnection.html',{'allclients': allclients, 'myconnectionslist': myconnectionslist,'profile_instances':profile_instances,'user_id':user,'myconnectionslistlimit':myconnectionslistlimit,'all_groups':all_groups})
#remove my friend from connection
class removeconnection(View):
    def get(self,request,cid):
        user = request.session['user_id']
        coninstance = Connections.objects.filter(id=cid).first()
        if coninstance:
            coninstance.is_active = False
            coninstance.save()
        return redirect('viewmyconnections1')
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from django.db.models import F, Value
from django.db.models.functions import Concat

class ChatViewPOST1(APIView):
    def post(self, request):
        serializer = ChatPostSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def view_chat_history1(request):
    if request.method == 'GET':
        fromid = request.GET.get('sender_id')
        print("chathistoryfromid",fromid)
        toid = request.GET.get('recipient_id')
        print("chathistorytoid",toid)
        # Fetch chat history based on sender and recipient IDs
        chats = Chat.objects.filter(Q(from_id=fromid, to_id=toid) | Q(from_id=toid, to_id=fromid)).order_by('created_at')
        # You might want to order the chats by created_at or any other criteria
        serializer = ChatSerializer(chats, many=True)
        return JsonResponse({'chats': serializer.data})

class ChatViewPOST1g(APIView):
    def post(self, request):
        serializer = ChatPostSerializerg(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def view_chat_history1g(request):
    if request.method == 'GET':
        fromid = request.GET.get('sender_id')
        print(fromid)
        toid = request.GET.get('recipient_id')
        print(toid)
        # Fetch chat history based on sender and recipient IDs
        chats = Chat.objects.filter(group_id=toid).order_by('created_at')
        # You might want to order the chats by created_at or any other criteria
        group=Wandergroup.objects.filter(id=toid,is_active=True).first()
        print(chats)
        serializer = ChatSerializer(chats, many=True)
        group_data = {
            'groupname': group.groupname,
            'groupdescription': group.groupdescription,
            'groupimage_url': group.groupimage.url,
        }

        return JsonResponse({'chats': serializer.data, 'group': group_data})

class Viewchatp(View):
    def get(self,request):
        user_id = request.session['user_id']
        fromiduser = Userprofile.objects.filter(id=user_id).first()
        print(fromiduser)
        distinct_chats = []


        if fromiduser:
            # Filter chat instances
            chat_instances = Chat.objects.filter(
                Q(from_id=fromiduser,group_id=None) | Q(to_id=fromiduser,group_id =None)
            ).order_by('created_at')

            # Use a set to store unique participant pairs
            unique_participants = set()

            for chat in chat_instances:
                participant_pair = tuple(sorted([chat.from_id_id, chat.to_id_id]))
                if participant_pair not in unique_participants:
                    unique_participants.add(participant_pair)

                    # Fetch client images for the participants with proper checks
                    from_client_image = None
                    to_client_image = None

                    if hasattr(chat.from_id, 'client') and chat.from_id.client.image:
                        from_client_image = chat.from_id.client.image

                    if hasattr(chat.to_id, 'client') and chat.to_id.client.image:
                        to_client_image = chat.to_id.client.image

                    # Append chat along with images to distinct_chats
                    distinct_chats.append({
                        'chat': chat,
                        'from_client_image': from_client_image,
                        'to_client_image': to_client_image,
                    })

            # Sort by the 'created_at' attribute of the 'chat' object within each dictionary
            distinct_chats.sort(key=lambda x: x['chat'].created_at, reverse=True)
            print(distinct_chats)

            return render(request, 'chatmain.html', {'chats': distinct_chats,'user_id':user_id})

            return render(request,'chatmain.html',{'chats':distinct_chats,})

        return render(request, 'chatmain.html', {'chats': []})
class Viewchatg(View):
    def get(self,request):
        user_id = request.session['user_id']
        fromiduser = Userprofile.objects.filter(id=user_id).first()
        print(fromiduser)
        distinct_chats = []

        assignedgroup_instances = Assignedgroups.objects.filter(user=fromiduser).all()
        for assignedgroup_instance in assignedgroup_instances:
            print(assignedgroup_instance.groupid.id)
            chat_instances = Chat.objects.filter(
                group_id__id=assignedgroup_instance.groupid.id).order_by('-created_at')

            # Use a set to store unique participant pairs
            unique_participants = set()

            for chat in chat_instances:
                participant_pair = tuple(sorted([chat.group_id_id]))
                if participant_pair not in unique_participants:
                    unique_participants.add(participant_pair)



                    from_client_image = None


                    if hasattr(chat.group_id, 'client') and chat.group_id.groupimage:
                        from_client_image = chat.group_id.groupimage



                    # Append chat along with images to distinct_chats
                    distinct_chats.append({
                        'chat': chat,


                    })

            # Sort by the 'created_at' attribute of the 'chat' object within each dictionary
        distinct_chats.sort(key=lambda x: x['chat'].created_at, reverse=True)
        print(distinct_chats)

        return render(request, 'chatgroups.html', {'chats': distinct_chats,'user_id':user_id})

        # return render(request,'client/chatmain.html',{'chats':distinct_chats,})

        # return render(request, 'client/chatmain.html', {'chats': []})
class Viewchatp1(View):
    def get(self,request,toid):
        user_id = request.session['user_id']
        fromiduser = Userprofile.objects.filter(id=user_id).first()
        print(fromiduser)
        distinct_chats = []

        if fromiduser:
            # Filter chat instances
            chat_instances = Chat.objects.filter(
                Q(from_id=fromiduser,group_id=None) | Q(to_id=fromiduser,group_id=None)
            ).order_by('created_at')

            # Use a set to store unique participant pairs
            unique_participants = set()

            for chat in chat_instances:
                participant_pair = tuple(sorted([chat.from_id_id, chat.to_id_id]))
                if participant_pair not in unique_participants:
                    unique_participants.add(participant_pair)

                    # Fetch client images for the participants with proper checks
                    from_client_image = None
                    to_client_image = None

                    if hasattr(chat.from_id, 'client') and chat.from_id.client.image:
                        from_client_image = chat.from_id.client.image

                    if hasattr(chat.to_id, 'client') and chat.to_id.client.image:
                        to_client_image = chat.to_id.client.image

                    # Append chat along with images to distinct_chats
                    distinct_chats.append({
                        'chat': chat,
                        'from_client_image': from_client_image,
                        'to_client_image': to_client_image,
                    })

            # Sort by the 'created_at' attribute of the 'chat' object within each dictionary
            distinct_chats.sort(key=lambda x: x['chat'].created_at, reverse=True)
            print(distinct_chats)
        print('toid', toid)
        fromid=request.session['user_id']
        print('fromid', fromid)
        fromiduser = Userprofile.objects.filter(id=fromid).first()
        toiduser = Userprofile.objects.filter(id=toid).first()
        toidimage=Client.objects.filter(user=toiduser).first()
        print('toidimage',toidimage)
        print(toiduser)
        print(fromiduser)
        chats = Chat.objects.filter(
            Q(from_id=fromiduser, to_id=toiduser) | Q(from_id=toiduser, to_id=fromiduser)).order_by('created_at')
        chats = chats.order_by('created_at')
        print("chatskkkkk", chats)  # Order by created_at
        serializer = ChatSerializer(chats, many=True)
        print(serializer)
        return render(request, 'chat.html', {'chats': serializer.data, 'to_id': toiduser,'chatss': distinct_chats,'user_id':user_id,'toidimage':toidimage})



class Viewchatg1(View):
    def get(self,request,groupid):
        user_id = request.session['user_id']
        fromiduser = Userprofile.objects.filter(id=user_id).first()
        print(fromiduser)
        wandergroup_instance=Wandergroup.objects.filter(user=fromiduser).first()
        distinct_chats = []

        assignedgroup_instances = Assignedgroups.objects.filter(user=fromiduser).all()
        for assignedgroup_instance in assignedgroup_instances:
            print(assignedgroup_instance.groupid.id)
            chat_instances = Chat.objects.filter(
                group_id__id=assignedgroup_instance.groupid.id).order_by('-created_at')

            # Use a set to store unique participant pairs
            unique_participants = set()

            for chat in chat_instances:
                participant_pair = tuple(sorted([chat.group_id_id]))
                if participant_pair not in unique_participants:
                    unique_participants.add(participant_pair)

                    from_client_image = None

                    if hasattr(chat.group_id, 'client') and chat.group_id.groupimage:
                        from_client_image = chat.group_id.groupimage

                    # Append chat along with images to distinct_chats
                    distinct_chats.append({
                        'chat': chat,

                    })

            # Sort by the 'created_at' attribute of the 'chat' object within each dictionary
        distinct_chats.sort(key=lambda x: x['chat'].created_at, reverse=True)
        print(distinct_chats)
        chats = Chat.objects.filter(group_id=groupid).order_by('created_at')
        chats = chats.order_by('created_at')
        print("chatskkkkk", chats)  # Order by created_at
        serializer = ChatSerializer(chats, many=True)
        print(serializer)
        return render(request,'chatgroupview.html',{'fromiduser':fromiduser,'chats': serializer.data, 'to_id': groupid,'chatss': distinct_chats,'user_id':user_id,'wandergroup_instance':wandergroup_instance})

class Chatviewpeoples(View):
    def get(self,request):
        print('chatviewpeoples')
        user_id=request.session['user_id']
        user_id=Userprofile.objects.filter(id=user_id).first()
        client_instances=Client.objects.filter(is_active=True).exclude(user=user_id).all()
        return render(request,'chatviewpeoples.html',{'chats':client_instances})
class Chatviewgroups(View):
    def get(self,request):
        print('chatviewgroups')
        user_id=request.session['user_id']
        user_id=Userprofile.objects.filter(id=user_id).first()
        assignedgroup_instances=Assignedgroups.objects.filter(user=user_id,is_active=True).all()
        return render(request,'chatviewgroups.html',{'chats':assignedgroup_instances})
from django.shortcuts import get_object_or_404
class Likeunlikepost(View):
    def post(self, request, id):
        # Retrieve the post instance
        print(id)
        post_instance = get_object_or_404(posts, id=id, is_active=True)

        user_id=request.session['user_id']
        user=Userprofile.objects.filter(id=user_id).first()

        # Check if a like already exists
        like_instance = Likepost.objects.filter(user=user, postid=post_instance).first()

        if like_instance:
            # Like exists, so delete it (unlike)
            like_instance.delete()
            like_status = False
        else:
            # Like does not exist, so create it (like)
            Likepost.objects.create(user=user, postid=post_instance, likestatus=True)
            like_status = True

        # Get the updated like count for the post
        like_count = Likepost.objects.filter(postid=post_instance).count()

        # Return the like status, like count, and post ID
        response_data = {
            'like_status': like_status,
            'like_count': like_count,
            'post_id': post_instance.id
        }

        return JsonResponse(response_data)


class Addcomment(View):
    def post(self,request):
        user_id=request.session['user_id']
        user_id=Userprofile.objects.filter(id=user_id,is_active=True).first()
        form = Addcommentform(request.POST)
        if form.is_valid():
            comment_instance=form.save(commit=False)
            comment_instance.user=user_id
            comment_instance.save()
            comment_data = {
                'id': comment_instance.id,
                'user': {
                    'id': comment_instance.user.id,
                    'username': comment_instance.user.first_name,  # adjust according to your user model
                    'image_url': comment_instance.user.client.image.url if comment_instance.user.client and comment_instance.user.client.image else None
                },
                'comment': comment_instance.comment,
                'created_at': comment_instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            return JsonResponse({'status': 'OK', 'comment': comment_data})

        return JsoResponse({'status': 'FAIL', 'errors': form.errors})
class Viewconnectionsprofile(View):
    def get(self,request,id):
        user = request.session['user_id']
        profile_instances = Userprofile.objects.filter(id=user).first()
        client_instance = Client.objects.filter(id=id).first()

        print('user',user)
        print('id',id)
        myconnection = Connections.objects.filter(
            Q(user_id=user, clientuserid_id=client_instance.user.id, is_active=True) |
            Q(user_id=client_instance.user.id, clientuserid_id=user, is_active=True)).first()
        print('myconnection',myconnection)
        if myconnection:

            client_instance = Client.objects.filter(id=id).first()
            # myconnectionslist = Connections.objects.filter(
                # Q(user=client_instance.user, is_active=True) |
                # Q(clientuserid=client_instance.user, is_active=True)).order_by('-id')
            myconnectionslist = Connections.objects.filter(
                Q(user=client_instance.user, is_active=True) |
                Q(clientuserid=client_instance.user, is_active=True)
            ).exclude(Q(user_id=user)|Q(clientuserid_id=user)).order_by('-id')
            created_groups = Wandergroup.objects.filter(user=client_instance.user, is_active=True)
            member_groups = Wandergroup.objects.filter( assignedgroups__is_active=True,assignedgroups__user=client_instance.user, is_active=True).exclude(user_id=user)

            print("hjhdsjkhf", member_groups)
            return render(request, 'commonprofile.html',
                          {'client_instance': client_instance, 'myconnectionslist': myconnectionslist,
                           'created_groups': created_groups, 'member_groups': member_groups})
        else:
            client_instance = Client.objects.filter(id=id).first()
            myconnectionslist = Connections.objects.filter(
                Q(user=client_instance.user, is_active=True) |
                Q(clientuserid=client_instance.user, is_active=True)
            ).exclude(Q(user_id=user)|Q(clientuserid_id=user)).order_by('-id')
            print('myconnectionslist',myconnectionslist)
            created_groups = Wandergroup.objects.filter(user=client_instance.user, is_active=True)
            member_groups = Wandergroup.objects.filter( assignedgroups__is_active=True,assignedgroups__user=client_instance.user, is_active=True).exclude(user_id=user)

            print("hjhdsjkhf", member_groups)
            return render(request, 'commonprofile1.html',
                          {'client_instance': client_instance, 'myconnectionslist': myconnectionslist,
                           'created_groups': created_groups, 'member_groups': member_groups})


#my grouprequest accept from viewmywandergroup
class mygrouprequestaccept(View):
    def get(self,request,id):
        assigngroup_instance=Assignedgroups.objects.filter(id=id).first()
        if assigngroup_instance:
            assigngroup_instance.is_active = True
            assigngroup_instance.save()
        return redirect('viewmywandergroup')


#requst page view
class loadrequestpage(View):
    def get(self,request):
        user = request.session['user_id']
        profile_instances = Userprofile.objects.filter(id=user).first()
        print(user)
        # join request to my groups
        user_groups = Wandergroup.objects.filter(user=profile_instances)
        # mygrouprequest = Assignedgroups.objects.filter(is_active=False, groupid__in=user_groups,groupaddmode='invite').exclude(groupid__user=profile_instances)
        mygrouprequest = Assignedgroups.objects.filter(is_active=False, user=profile_instances,
                                                       groupaddmode='invite').exclude(groupid__user=profile_instances)

        print('mygrouprequest',mygrouprequest)
        myconnectionrwquests=Connections.objects.filter(clientuserid=user,is_active=False)
        # member_grouprequest = Wandergroup.objects.filter(Assignedgroups__user=user,Assignedgroups__is_invited=False, aAssignedgroups__is_active=False,is_active = True)
        print("myconnectionrwquests")
        print(myconnectionrwquests)
        member_grouprequest = Wandergroup.objects.filter(
            assignedgroups__user=user,
            assignedgroups__is_invited=True,
            assignedgroups__is_active=False,
            is_active=True
        )

        print(member_grouprequest)

        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                            is_active=True).order_by('-id')[:10]
        print("postconnectionlimit")
        print(myconnectionslistlimit)

        created_groups = Wandergroup.objects.filter(user=user, is_active=True)

        # Get groups where the user is a member
        member_groups = Wandergroup.objects.filter(assignedgroups__user=user, assignedgroups__is_active=True, is_active=True)

        # Combine both querysets
        all_groups = Wandergroup.objects.filter(
            Q(user=user) | Q(assignedgroups__user=user),
            is_active=True
        ).distinct()
        return render(request,'requestview.html',{'user_id':user,'mygrouprequest': mygrouprequest, 'myconnectionrwquests': myconnectionrwquests,'member_grouprequest':member_grouprequest,'myconnectionslistlimit':myconnectionslistlimit,'all_groups':all_groups,'profile_instances':profile_instances})

#delete my connectionrequest

class deletemyconnectionrequest(View):
    def get(self,requst,id):
        connection_instance = Connections.objects.filter(id=id).first()
        if connection_instance:
            connection_instance.delete()
        return redirect('loadrequestpage')


class mygrouprequestreject(View):
    def get(self,requst,id,gid):

        print("reject")
        assign_instance = Assignedgroups.objects.filter(user_id=id,groupid=gid).first()
        print('assign_instance',assign_instance)

        if assign_instance:
            print("reject")
            assign_instance.delete()

        return redirect('viewmywandergroup')

class acceptmyconnectionrequest(View):
    def get(self,requst,id):
        connection_instance = Connections.objects.filter(id=id).first()
        if connection_instance:
            connection_instance.is_active = True
            connection_instance.save()
        return redirect('loadrequestpage')


# accept group invitation
# acceptinvitation
class acceptinvitation(View):
    def get(self,request,id):
        print('requestid',id)
        user=request.session['user_id']
        user_instance=Userprofile.objects.filter(id=id).first()
        print(id)
        print(user)
        assign_instance = Assignedgroups.objects.filter(id=id).first()
        print('assign-instance',assign_instance)
        if assign_instance:
            assign_instance.is_active = True
            assign_instance.save()
        return redirect('loadrequestpage')

#invite friends for my group


class InviteFriendsView(View):
    def post(self, request, id):
        # For debugging
        print(id)
        print(request.POST)
        print("okkkkkkkkkkkk")

        friend_ids = request.POST.getlist('friends')
        # For debugging
        print(friend_ids)

        group_id = id  # Use the actual group ID passed in the URL

        for friend_id in friend_ids:
            friend_profile = Userprofile.objects.get(id=friend_id)
            Assignedgroups.objects.create(
                user=friend_profile,
                groupid_id=group_id,
                status=False,
                groupaddmode='invite',
                is_active=False,
                is_invited=True
            )
        return redirect(reverse('viewwandergroup', args=[group_id]))
        # Replace with your success URL or page

    def get(self, request, id):
        # Handle GET requests if necessary
        return redirect(reverse('viewwandergroup', args=[id]))
class SearchSuggestionsView(View):
    def get(self, request, *args, **kwargs):
        print('hello')
        query = request.GET.get('q', '')
        if query:
            if query.startswith('#'):
                stripped_query = query.lstrip('#')
                hashtags = hashtag.objects.filter(hashtag__icontains=stripped_query, is_active=True).values()[:5]
                grouphashtags=grouphashtag.objects.filter(hashtag__icontains=stripped_query, is_active=True).values()[:5]
                suggestions = {
                    'hashtags': [],
                    'posts': list(hashtags),
                    'groups': list(grouphashtags),
                    'clients': [],
                    'people': [],
                    'places': [],
                }
            else:
                pos = posts.objects.filter(postcontent__icontains=query, is_active=True).values()[:5]
                # hashtags = hashtag.objects.filter(hashtag__icontains=query, is_active=True).values()[:5]
                groups = Wandergroup.objects.filter(groupname__icontains=query, is_active=True).values()[:5]
                clients = Client.objects.filter(user__first_name__icontains=query, is_active=True).values()[:5]
                people = Client.objects.filter(user__first_name__icontains=query, is_active=True).values()[:5]
                places = placevisited.objects.filter(placename__icontains=query).values()[:5]


                suggestions = {
                    'posts': list(pos),

                    'groups': list(groups),
                    'clients': list(clients),
                    'people': list(people),
                    'places': list(places),
                }
        else:
            suggestions = {'posts': [], 'hashtags': [], 'groups': [], 'clients': [], 'places': [],'people': []}
        print(suggestions)
        return JsonResponse(suggestions)

class Postviewbysearch(View):
    def get(self, request, postname):
        user = request.session.get('user_id')
        profile_instances = Userprofile.objects.filter(id=user).first()
        member_group_ids = Assignedgroups.objects.filter(user=user).values_list('groupid_id', flat=True)

        # Exclude groups that are either created by the user or where the user is a member
        # available_groups = Wandergroup.objects.filter(is_active=True, id__in=group_ids, ).exclude(
        #     id__in=created_group_ids.union(member_group_ids))
        # all my groups
        # created_groups = Wandergroup.objects.filter(user=user, id__in=group_ids, is_active=True)
        # member_groups = Wandergroup.objects.filter(assignedgroups__user=user, id__in=group_ids,
        #                                            is_active=True)
        created_groups = Wandergroup.objects.filter(user=user, is_active=True)
        member_groups = Wandergroup.objects.filter( assignedgroups__user=user, assignedgroups__is_active=True,
                                                   is_active=True)
        # Combine both querysets
        all_groups = created_groups | member_groups
        if postname.startswith('#'):
            # Fetch post instances from hashtag model
            stripped_query = postname.lstrip('#')
            post_instances = posts.objects.filter(
                id__in=hashtag.objects.filter(
                    hashtag__icontains=stripped_query, is_active=True
                ).values_list('post_id', flat=True),
                is_active=True
            )
            print('#tagposts',post_instances)
        else:
            # Fetch post instances from posts model
            post_instances = posts.objects.filter(
                postcontent__icontains=postname, is_active=True
            ).all()
        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                            is_active=True).order_by('-id')[:10]
        return render(request, 'postviewbysearch.html', {'all_groups': all_groups,'post_instances': post_instances,'myconnectionslistlimit':myconnectionslistlimit,'profile_instances':profile_instances})

class Groupviewbysearch(View):
    def get(self, request, groupname):
        user = request.session.get('user_id')
        profile_instances = Userprofile.objects.filter(id=user).first()

        if groupname.startswith('#'):
            # Remove the leading '#' for the search
            stripped_groupname = groupname.lstrip('#')
            # Fetch group instances based on hashtags
            group_ids = grouphashtag.objects.filter(hashtag__icontains=stripped_groupname, is_active=True).values_list(
                'group_id', flat=True)
            group_instances = Wandergroup.objects.filter(id__in=group_ids, is_active=True)
            print('group_instances',group_instances)
            created_group_ids = Wandergroup.objects.filter(user=user, id__in=group_ids,).values_list('id',flat=True)
            myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                                is_active=True).order_by('-id')[:10]
            # Get groups where the user is a member
            member_group_ids = Assignedgroups.objects.filter(user=user).values_list('groupid_id', flat=True)

            # Exclude groups that are either created by the user or where the user is a member
            available_groups = Wandergroup.objects.filter(is_active=True, id__in=group_ids,).exclude(
                id__in=created_group_ids.union(member_group_ids))
            # all my groups
            created_groups = Wandergroup.objects.filter(user=user, id__in=group_ids, is_active=True)
            member_groups = Wandergroup.objects.filter( assignedgroups__user=user, assignedgroups__is_active=True, id__in=group_ids,
                                                       is_active=True).exclude(user_id=user)

            # Combine both querysets
            all_groups = created_groups | member_groups
            # /all_groups = all_groups.distinct()
        else:
            # Fetch group instances based on groupname
            group_instances = Wandergroup.objects.filter(groupname__icontains=groupname, is_active=True)
        # all groups exclude me
            created_group_ids = Wandergroup.objects.filter(user=user, groupname__icontains=groupname).values_list('id',
                                                                                                                  flat=True)
            myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                                is_active=True).order_by('-id')[:10]
            # Get groups where the user is a member
            member_group_ids = Assignedgroups.objects.filter(user=user).values_list('groupid_id', flat=True)

            # Exclude groups that are either created by the user or where the user is a member
            available_groups = Wandergroup.objects.filter(is_active=True, groupname__icontains=groupname).exclude(
                id__in=created_group_ids.union(member_group_ids))

            # all my groups
            created_groups = Wandergroup.objects.filter(user=user, groupname__icontains=groupname, is_active=True)
            member_groups = Wandergroup.objects.filter( assignedgroups__user=user, assignedgroups__is_active=True ,groupname__icontains=groupname,
                                                       is_active=True).exclude(user_id=user)

            # Combine both querysets
            all_groups = created_groups | member_groups
        # join request to my groups
        user_groups = Wandergroup.objects.filter(user=profile_instances, groupname__icontains=groupname)
        mygrouprequest = Assignedgroups.objects.filter(is_active=False, groupid__in=user_groups)



        # /all_groups = all_groups.distinct()

        myconnectionslist = Connections.objects.filter(user=user, is_active=True).order_by('-id')
        wandergroup_instances1 = Wandergroup.objects.filter(is_active=True, groupname__icontains=groupname)

        mygroups = Wandergroup.objects.filter(user__id=user, is_active=True).order_by('-id')


        return render(request, 'groupviewbysearch.html', {
            'user_id':user,
            'wandergroup_instances': available_groups,
            'profile_instances': profile_instances,
            'myconnectionslist': myconnectionslist,
            'all_groups': all_groups,
            'created_groups': created_groups,
            'member_groups': member_groups,
            'myconnectionslistlimit': myconnectionslistlimit,
            'mygrouprequest': mygrouprequest
        })

class Peopleviewbysearch(View):
    def get(self,request,people):
        user = request.session['user_id']
        print(user)
        user1 = Userprofile.objects.filter(id=user).first()
        print(user1)
        member_group_ids = Assignedgroups.objects.filter(user=user).values_list('groupid_id', flat=True)

        # Exclude groups that are either created by the user or where the user is a member
        # available_groups = Wandergroup.objects.filter(is_active=True, id__in=group_ids, ).exclude(
        #     id__in=created_group_ids.union(member_group_ids))
        # all my groups
        created_groups = Wandergroup.objects.filter(user=user, is_active=True)
        member_groups = Wandergroup.objects.filter( assignedgroups__user=user, assignedgroups__is_active=True,
                                                   is_active=True)

        # Combine both querysets
        all_groups = created_groups | member_groups
        # profile_instance = Client.objects.filter(is_active=True, user=user_profile).first()
        profile_instances = Userprofile.objects.filter(id=user).first()
        print(profile_instances)
        print(profile_instances.email)
        connected_client_ids = Connections.objects.filter(Q(is_active=True,user_id=user) | Q(is_active=True,clientuserid_id=user),
                                                       is_active=True).values_list('client_id', flat=True)
        # profile_instances = Client.objects.filter(is_active=True, user=user1).first()
        allclients = Client.objects.filter(user__first_name__icontains=people,is_active=True).exclude(user=user).exclude(id__in=connected_client_ids)
        # connection_instances = Connections.objects.filter(Q(user__id=request.session['user_id'],is_active=True)|Q(clientuserid=user,is_active=True)).all()
        # myconnectionslist = Connections.objects.filter(user__id=user, is_active=True).all().order_by('-id')
        myconnectionslist = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                       is_active=True).order_by('-id')

        people_instances=Client.objects.filter(user__first_name__icontains=people, is_active=True).all()
        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                       is_active=True).order_by('-id')[:10]
        # remove my friend from connection
        return render(request,'peopleviewbysearch.html',{'allclients': allclients,'myconnectionslistlimit':myconnectionslistlimit ,'myconnectionslist': myconnectionslist,
                       'profile_instances': profile_instances,'all_groups':all_groups})


class Connectionsviewbysearch(View):
    def get(self, request, connection):
        user = request.session['user_id']
        user1 = Userprofile.objects.filter(id=user).first()
        # profile_instance = Client.objects.filter(is_active=True, user=user_profile).first()
        profile_instances = Userprofile.objects.filter(id=user).first()
        member_group_ids = Assignedgroups.objects.filter(user=user).values_list('groupid_id', flat=True)

        # Exclude groups that are either created by the user or where the user is a member
        # available_groups = Wandergroup.objects.filter(is_active=True, id__in=group_ids, ).exclude(
        #     id__in=created_group_ids.union(member_group_ids))
        # all my groups
        created_groups = Wandergroup.objects.filter(user=user, is_active=True)
        member_groups = Wandergroup.objects.filter( assignedgroups__user=user, assignedgroups__is_active=True,
                                                   is_active=True)
        # created_groups = Wandergroup.objects.filter(user=user, id__in=group_ids, is_active=True)
        # member_groups = Wandergroup.objects.filter(assignedgroups__user=user, id__in=group_ids,
        #                                            is_active=True)

        # Combine both querysets
        all_groups = created_groups | member_groups

        connected_client_ids = Connections.objects.filter(Q(is_active=True,user_id=user) | Q(is_active=True,clientuserid_id=user),
                                                       is_active=True).values_list('client_id', flat=True)
        print('connected_client_ids',connected_client_ids)
        # profile_instances = Client.objects.filter(is_active=True, user=user1).first()
        allclients = Client.objects.filter(is_active=True).exclude(user=user).exclude(id__in=connected_client_ids)
        # connection_instances = Connections.objects.filter(Q(user__id=request.session['user_id'],is_active=True)|Q(clientuserid=user,is_active=True)).all()
        # myconnectionslist = Connections.objects.filter(user__id=user, is_active=True).all().order_by('-id')
        print('connection',connection)
        myconnectionslist = Connections.objects.filter(
            (Q(user__first_name__icontains=connection, clientuserid=user1, user__is_active=True) |
             Q(clientuserid__first_name__icontains=connection, user=user1  ,clientuserid__is_active=True)),
            is_active=True
        ).order_by('-id')

        connection_instances=Connections.objects.filter(Q(user__first_name__icontains=connection, is_active=True)|Q(clientuserid__first_name__icontains=connection, is_active=True)).all()
        print('connection_instances',myconnectionslist)
        myconnectionslistlimit = Connections.objects.filter(Q(user_id=user) | Q(clientuserid_id=user),
                                                       is_active=True).order_by('-id')[:10]
        return render(request,'connectionsviewbysearch.html',{'user_id':user,'allclients': allclients,'myconnectionslistlimit':myconnectionslistlimit ,
                                                              'myconnectionslist': myconnectionslist,'profile_instances':profile_instances,'all_groups':all_groups})
class Addconnections1(View):
    def get(self,request,id):

        user_id = request.session['user_id']
        user_id = Userprofile.objects.filter(id=user_id, is_active=True).first()
        connected_client_ids = Connections.objects.filter(Q(user__id=request.session['user_id'],is_active=True)|Q(clientuserid=user_id,is_active=True)).values_list('client_id',
                                                                                                         flat=True)
        client_instance=Client.objects.filter(user__id=id).first()
        print('client_instance',client_instance)
        # Exclude connected clients from the list of available users
        user_instances = Client.objects.filter(is_active=True).exclude(user=user_id).exclude(
            id__in=connected_client_ids)
        clientuserid = Userprofile.objects.filter(id=id, is_active=True).first()
        print(clientuserid)
        Connections.objects.create(user=user_id, client=client_instance, clientuserid=clientuserid, is_active=False)

        # return render(request, 'addconnections.html',
        #               {'user_instances': user_instances})
        return redirect('viewmyconnections1')


class Chatviewpeoples1(View):
    def get(self, request):
        print('chatviewpeoples')
        user_id = request.session.get('user_id')
        user_profile = Userprofile.objects.filter(id=user_id).first()

        search_query = request.GET.get('search', '')
        if search_query:
            client_instances = Client.objects.filter(
                is_active=True,
                user__first_name__icontains=search_query
            ).exclude(user=user_profile)
        else:
            client_instances = Client.objects.filter(
                is_active=True
            ).exclude(user=user_profile)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'clients': [{
                    'id': client.user.id,
                    'first_name': client.user.first_name,
                    'image_url': client.image.url
                } for client in client_instances]
            })

        return render(request, 'chatviewpeoples.html', {'chats': client_instances})
class Verfiyphonemail(View):
    def get(self,request):
        print('hello')
        return render(request,'verifyphonemail.html')

class Verifyphonemail2(View):
    def get(self, request):
        form = ClientRegistrationForm()
        return render(request, '2verifyphonemail.html', {'form': form})
    def post(self, request):
        print('post')
        print(request.user.id)
        print('first_name',request.POST['first_name'])
        print('second_name',request.POST['second_name'])


        user_instance=Userprofile.objects.filter(id=request.user.id,is_active=True).first()
        client_instance=Client.objects.filter(user=user_instance).first()
        form = ClientRegistrationForm2(request.POST, request.FILES,instance=client_instance)
        print(client_instance)
        # hashpass=make_password()
        if form.is_valid():
            client_instance = form.save(commit=False)
            user=client_instance.user

            user.first_name=request.POST['first_name']
            user.second_name = request.POST['second_name']

            user.save()
            client_instance.save()


            return redirect('userlogin')
        return render(request, 'register.html', {'form': form})


from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Userprofile

@method_decorator(csrf_exempt, name='dispatch')
class CheckUniqueView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')

        is_unique_username = not Userprofile.objects.filter(username=username).exists()
        is_unique_email = not Client.objects.filter(email=email).exists()

        return JsonResponse({
            'is_unique': is_unique_username and is_unique_email,
            'is_unique_username': is_unique_username,
            'is_unique_email': is_unique_email
        })

    def get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Invalid request method'}, status=400)

import json
import random
import string
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
from .models import Userprofile
from datetime import datetime, timedelta

# Helper function to generate OTP
def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

# Simulate sending OTP via SMS (this should be replaced with actual SMS sending logic)
def send_sms(phone_number, otp):
    print(f"Sending SMS to {phone_number}: Your OTP is {otp}")
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=f"Wander Connect Your verification code is {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )

@method_decorator(csrf_exempt, name='dispatch')
class SendOtpView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password= data.get('password')
        print('username',username)
        print('email',email)
        print('phone_number',phone_number)
        print('password',password)

        # Generate OTPs
        email_otp = generate_otp()
        phone_otp = generate_otp()
        print('email_otp',email_otp)
        print('phone_otp',phone_otp)
        # Save OTPs in session (or any other temporary storage)
        request.session['username'] = username
        request.session['email'] = email
        request.session['phone_number'] = phone_number
        request.session['password'] = password
        request.session['email_otp'] = email_otp
        request.session['phone_otp'] = phone_otp
        request.session['otp_expiry'] = (datetime.now() + timedelta(minutes=10)).isoformat()

        # Send OTPs
        send_mail(
            'Your Email OTP',
            f'Your OTP for email verification is {email_otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        send_sms(phone_number, phone_otp)

        return JsonResponse({'message': 'OTP sent successfully'})
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
@method_decorator(csrf_exempt, name='dispatch')
class VerifyOtpView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        email_otp = data.get('email_otp')
        phone_otp = data.get('phone_otp')

        # Retrieve OTPs from session
        stored_email_otp = request.session.get('email_otp')
        stored_phone_otp = request.session.get('phone_otp')
        otp_expiry = datetime.fromisoformat(request.session.get('otp_expiry'))

        if datetime.now() > otp_expiry:
            return JsonResponse({'message': 'OTP has expired'}, status=400)

        if email_otp == stored_email_otp and phone_otp == stored_phone_otp:

            # Save user to the database or perform any other desired action
            # (Add your user creation logic here)

            print('user_id',request.user.id)
            username = request.session.get('username')
            email = request.session.get('email')
            phone_number = request.session.get('phone_number')
            password = request.session.get('password')
            user = Userprofile.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type='CLIENT',
            )
            Client.objects.create(
                user=user,
                phone_number=phone_number,
                email=email
            )
            login(request, user)
            return JsonResponse({'message': 'OTP verified successfully'})
        else:
            return JsonResponse({'message': 'Invalid OTP'}, status=400)