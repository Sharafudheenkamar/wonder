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
        all_groups = created_groups | member_groups
        print(all_groups)


        print(mygroups3)
        # Create a dictionary to track likes by the current user
        user_likes = Likepost.objects.filter(user=user_profile, postid__in=allpost).values_list('postid', flat=True)
        user_likes_dict = {post_id: True for post_id in user_likes}
        post_data = []
        for post in allpost:
            client_image_url = post.user.client.image.url if post.user.client and post.user.client.image else None
            comments = Commentpost.objects.filter(postid=post, is_active=True).order_by('created_at')
            post_data.append({
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
