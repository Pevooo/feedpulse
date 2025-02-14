using AutoMapper;

namespace Api.Core.Mapping.Users
{
    public partial class UserProfile : Profile
    {
        public UserProfile()
        {
            AddUserMapping();
            GetUserByIdMapping();
            GetUserPaginationMapping();
        }
    }
}
