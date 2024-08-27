from users.models import MembershipClaim
from rest_framework import generics, permissions
from users.serializers import MembershipClaimSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.managers import UserManager
from users.serializers import UserCardSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from users.permissions import IsRoleGSOrPresident

class MembershipClaimView(APIView):
    queryset = MembershipClaim.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = MembershipClaimSerializer(data={**request.data, 'claimant': request.user.id})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(claimant=self.request.user)

        # Send success message to requesting user
        return Response({'message': 'Claim created successfully!'})
    
class MembershipClaimList(generics.ListAPIView):
    serializer_class = MembershipClaimSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = MembershipClaim.objects.all()

        page_size = self.request.query_params.get('page_size', None)
        
        if page_size :
            self.pagination_class = PageNumberPagination
            self.pagination_class.page_size = int(page_size)
        else:
            self.pagination_class = None

        return queryset

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser, IsRoleGSOrPresident])
def accept_membership_claim(request, id):
    """
    API endpoint to accept or decline a pending user.
    Only superusers can access this method.
    """
    try:
        # Check if claim exists
        claim = MembershipClaim.objects.get(id=id)

        is_accepted = request.data.get("accept")
        
        if is_accepted:
            UserManager().changeMembership(claim.claimant, claim.category)
        
        # Serialize and return user data
        serializer = UserCardSerializer(claim.claimant)

        claim.delete()

        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except MembershipClaim.DoesNotExist:
        return Response({'error': 'Claim not found'}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
