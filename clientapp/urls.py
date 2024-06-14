from django.urls import path
from .views import *

urlpatterns = [
    path('addwandergroup/',Addwandergroup.as_view(),name='addwandergroup'),

    path('register/', ClientRegistrationView.as_view(), name='client_register'),
    path('loadaddplacevisited',loadaddplacevisited.as_view(),name='loadaddplacevisited'),
    path('viewmyvisitedplace',ViewMyVisitedPlace.as_view(),name='viewmyvisitedplace'),
    # path('geteditvisitedplace/<str:data>',geteditvisitedplace.as_view(),name='geteditvisitedplace'),
    # path('deletevistedplaces/<str:data>',deletevistedplaces.as_view(),name='deletevistedplaces'),
    # path('add_place',add_place.as_view(),name='add_place'),
    path('viewmyprofile',viewmyprofile.as_view(),name='viewmyprofile'),
    path('editmyprofile/<str:id>',editmyprofile.as_view(),name='editmyprofile'),
    path('loadaddpost',loadaddpost.as_view(),name='loadaddpost'),
    path('changepassword',changepassword.as_view(),name='changepassword'),
    path('viewmypost',viewmypost.as_view(),name='viewmypost'),
    path('deletepost/<str:id>',deletepost.as_view(),name='deletepost'),
    path('editpost/<str:id>',editpost.as_view(),name='editpost'),
    path('removeconnection/<str:cid>',removeconnection.as_view(),name='removeconnection'),
    path('mygrouprequestreject/<str:id>/<str:gid>',mygrouprequestreject.as_view(),name='mygrouprequestreject'),

    path('addwandergroup/',Addwandergroup.as_view(),name='addwandergroup'),
    path('viewwandergroup/<str:id>',Viewwandergroup.as_view(),name='viewwandergroup'),
    path('viewwandergroup1/<str:id>', Viewwandergroup1.as_view(), name='viewwandergroup1'),

    path('viewmywandergroup',viewmywandergroup.as_view(),name='viewmywandergroup'),
    path('mygrouprequestaccept/<str:id>',mygrouprequestaccept.as_view(),name='mygrouprequestaccept'),
    path('editwandergroup/<id>',Editewandergroup.as_view(),name='editwandergroup'),
    path('deletewandergroup/<id>',Deletewandergroup.as_view(),name='deletewandergroup'),
    path('loadaddgrouppost/<str:id>',loadaddgrouppost.as_view(),name='loadaddgrouppost'),
    path('loadaddgrouppost', loadaddgrouppost.as_view(), name='loadaddgrouppost1'),
    path('gropuyoucanjoinindetail/<str:id>',gropuyoucanjoinindetail.as_view(),name='gropuyoucanjoinindetail'),
    path('joingrouprequest/<str:gid>',joingrouprequest.as_view(),name='joingrouprequest'),
    path('join/<str:grouplink>', join_group, name='join_group'),
    path('join/<str:grouplink>', join_group2, name='join_group2'),
    path('join/<str:grouplink>/join2', join_group, name='join_group2'),
    path('sharelink/<id>',Sharelink.as_view(),name='sharelink'),
    path('sharelink/',Sharelink.as_view(),name='sharelink'),
    path('invitelink/<id>',Invitelink.as_view(),name='invitelink'),
    path('invitelink/', Invitelink.as_view(), name='invitelink'),
    path('changeimage',changeimage.as_view(),name='changeimage'),
    path('addconnections/',Addconnections.as_view(),name='addconnections'),

    path('viewconnections/',Viewconnections.as_view(),name='viewconnections'),
    #remvoveconnections
    path('removeconnections/<id>',Viewconnections.as_view(),name='removeconnections'),
    #viewinvitations
    path('viewinvitations/',Viewinvitations.as_view(),name='viewinvitations'),
    #view sharelinks
    path('viewsharelinks/', Viewsharelinks.as_view(), name='viewsharelinks'),

    path('viewmembergroups/',Viewmembergroups.as_view(),name='viewmembergroups'),
    path('viewmyconnections1/',viewmyconnections1.as_view(),name='viewmyconnections1'),

    path('trainerchatpost/', ChatViewPOST1.as_view(), name='send_message'),

    path('view_chat_history/', view_chat_history1, name='view_chat_history'),

    path('trainerchatpostg/', ChatViewPOST1g.as_view(), name='send_message'),
    path('view_chat_historyg/', view_chat_history1g, name='view_chat_history'),

    path('viewchatp/', Viewchatp.as_view(), name='viewchatp'),
    path('viewchatg/', Viewchatg.as_view(), name='viewchatg'),

    path('viewchatp1/<toid>', Viewchatp1.as_view(), name='viewchatp1'),
    path('viewchatg1/<groupid>', Viewchatg1.as_view(), name='viewchatg1'),

    path('chatviewpeoples/',Chatviewpeoples.as_view(),name='chatviewpeoples'),
    path('chatviewgroups/',Chatviewgroups.as_view(),name='chatviewgroups'),

    path('likeunlikepost/<id>/',Likeunlikepost.as_view(),name='likeunlikepost'),
    path('addcomment/',Addcomment.as_view(),name='addcomment'),
    path('viewconnectionsprofile/<id>',Viewconnectionsprofile.as_view(),name='viewconnectionsprofile'),
    path('loadrequestpage/',loadrequestpage.as_view(),name='loadrequestpage'),
    path('acceptmyconnectionrequest/<str:id>',acceptmyconnectionrequest.as_view(),name='acceptmyconnectionrequest'),
    path('deletemyconnectionrequest/<str:id>',deletemyconnectionrequest.as_view(),name='deletemyconnectionrequest'),
    path('invite_friends/<str:id>',InviteFriendsView.as_view(),name='invite_friends'),
    path('acceptinvitation/<str:id>',acceptinvitation.as_view(),name='acceptinvitation'),

    #search
    path('search_suggestions/', SearchSuggestionsView.as_view(), name='search_suggestions'),
    path('postviewbysearch/<postname>/', Postviewbysearch.as_view(), name='postviewbysearch'),
    path('groupviewbysearch/<groupname>/', Groupviewbysearch.as_view(), name='groupviewbysearch'),
    path('peopleviewbysearch/<people>/', Peopleviewbysearch.as_view(), name='peopleviewbysearch'),
    path('connectionsviewbysearch/<connection>/', Connectionsviewbysearch.as_view(), name='connectionsviewbysearch'),
    path('addconnections/<id>', Addconnections1.as_view(), name='addconnections1'),
    path('chatviewpeoples1/',Chatviewpeoples1.as_view(),name='chatviewpeoples1'),
    path('verifyphonemail/',Verfiyphonemail.as_view(),name='verifyphonemail'),
    # path('verifyphonemailotp/',Verfiyphonemailotp.as_view(),name='verifyphonemailotp'),
    path('check-unique/', CheckUniqueView.as_view(), name='check_unique'),
    path('send-otp/', SendOtpView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),
    path('2verifyphonemail/', Verifyphonemail2.as_view(), name='2verifyphonemail'),
]