from django.urls import path
from users.views import obtain_auth_token, logout,google_signin
from . import views

urlpatterns = [
    # Authentication endpoints
    path('login/', obtain_auth_token, name='token_obtain_pair'),
    path('google-signin/', google_signin, name='google-signin'),# Endpoint for obtaining an authentication token
    path('logout/',logout, name='logout'),  # Endpoint for logging out a user
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'), # endpoint for changing password
    path('reset-password/', views.ResetPassword.as_view(), name='reset_password'), # endpoint for resetting password
    path('reset-password/confirm/', views.ResetPasswordConfirmation.as_view(), name='confirm_reset_password'), # endpoint for resetting password
    
    # Endpoint to make a user an admin
    path('make-admin/', views.make_admin, name='make_admin'),
    path('set-role/', views.set_role, name='set_role'),
    # Endpoint to remove adminship from a user
    path('remove-admin/<str:username>/', views.remove_admin, name='remove_admin'),

    # User endpoints
    path('user/', views.SelfUserDetail.as_view(), name='user_self'),  # Endpoint for retrieving self user information
    path('create/users/', views.UserCreate.as_view(), name='user_create'),  # Endpoint for creating a new user\
    path('users/', views.UserList.as_view(), name='user_list'),  # Endpoint for retrieving a list of users
    path('pending-users/', views.PendingUserList.as_view(), name='pending_user_list'),  # Endpoint for retrieving a list of users
    path('pending-users/<str:username>/', views.accept_pending, name='accept_pending_user'),  # Endpoint for retrieving a list of users
    path('users/<str:username>/', views.UserDetail.as_view(), name='user_detail'),  # Endpoint for retrieving user details by username
    path('users/<str:username>/change-membership/', views.change_membership, name='user_change_membership'),
    

    # Profile endpoints
    path('basic-profile/', views.SelfProfileDetail.as_view(), name='basic_profile_self'),  # Endpoint for retrieving self profile information
    path('basic-profiles/', views.ProfileList.as_view(), name='basic_profile_list'),  # Endpoint for retrieving a list of profiles
    path('basic-profiles/<str:username>/', views.ProfileDetail.as_view(), name='basic_profile_detail'),  # Endpoint for retrieving profile details by username

    # Referral endpoint
    path('referrals/create/', views.ReferralCreate.as_view(), name='referral_create'),  # Endpoint for creating a referral

    # Social media link endpoints
    path('profile/social-media-links/', views.SocialMediaLinkListView.as_view(), name='social-media-links'),  # Endpoint for retrieving social media links for a profile
    path('profile/create/social-media-links/', views.SocialMediaLinkCreateView.as_view(), name='create-social-media-link'),  # Endpoint for creating a social media link for a profile

    # Present address endpoints
    path('profile/present-address/', views.PresentAddressDetailView.as_view(), name='present-address'),  # Endpoint for retrieving present address for a profile
    path('profile/create/present-address/', views.PresentAddressCreateView.as_view(), name='create-present-address'),  # Endpoint for creating a present address for a profile

    # Skill endpoints
    path('profile/skills/', views.SkillListView.as_view(), name='skills'),  # Endpoint for retrieving skills for a profile
    path('profile/create/skills/', views.SkillCreateView.as_view(), name='create-skill'),  # Endpoint for creating a skill for a profile

    # Work experience endpoints
    path('profile/work-experiences/', views.WorkExperienceListView.as_view(), name='work-experiences'),  # Endpoint for retrieving
    path('profile/create/work-experiences/', views.WorkExperienceCreateView.as_view(), name='create-work-experience'),  # Create a new work experience

    # Academic Histories
    path('profile/academic-histories/', views.AcademicHistoryListView.as_view(), name='academic-histories'),  # Retrieve list of academic histories
    path('profile/create/academic-histories/', views.AcademicHistoryCreateView.as_view(), name='create-academic-history'),  # Create a new academic history

    # Detail Views
    path('profile/social-media-links/<int:pk>/', views.SocialMediaLinkDetailView.as_view(), name='social-media-link-detail'),  # Retrieve details of a social media link by primary key
    path('profile/skills/<int:pk>/', views.SkillDetailView.as_view(), name='skill-detail'),  # Retrieve details of a skill by primary key
    path('profile/work-experiences/<int:pk>/', views.WorkExperienceDetailView.as_view(), name='work-experience-detail'),  # Retrieve details of a work experience by primary key
    path('profile/academic-histories/<int:pk>/', views.AcademicHistoryDetailView.as_view(), name='academic-history-detail'),  # Retrieve details of an academic history by primary key

    # User-Specific Views
    path('profiles/<str:username>/social-media-links/', views.SocialMediaLinkUserListView.as_view(), name='user-social-media-links'),  # Retrieve social media links for a user by username
    path('profiles/<str:username>/skills/', views.SkillUserListView.as_view(), name='user-skills'),  # Retrieve skills for a user by username
    path('profiles/<str:username>/work-experiences/', views.WorkExperienceUserListView.as_view(), name='user-work-experiences'),  # Retrieve work experiences for a user by username
    path('profiles/<str:username>/academic-histories/', views.AcademicHistoryUserListView.as_view(), name='user-academic-histories'),  # Retrieve academic histories for a user by username
    path('profiles/<str:username>/present-address/', views.PresentAddressUserDetailView.as_view(), name='user-present-address'),  # Retrieve present address for a user by username

    # Own Profile View
    path('profile/', views.OwnFullProfileView.as_view(), name='own_full_profile'),  # Retrieve full profile information for the authenticated user's own profile

    # Full Profile View
    path('profiles/<str:username>/', views.FullProfileDetail.as_view(), name='full_profile_detail'),  # Retrieve full profile information of a user by username

    path('membership-claim/', views.MembershipClaimView.as_view(), name='membership_claim'), 
    path('membership-claim/<int:id>/', views.accept_membership_claim, name='accept_membership_claim'),

    path('membership-claims/', views.MembershipClaimList.as_view(), name='membership_claim_list'), 
]
