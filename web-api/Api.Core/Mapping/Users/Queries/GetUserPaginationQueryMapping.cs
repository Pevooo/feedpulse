using Api.Core.Features.Users.Queries.Response;
using Api.Data.Entities.Identity;

namespace Api.Core.Mapping.Users
{
    public partial class UserProfile
    {
        public void GetUserPaginationMapping()
        {
            _ = CreateMap<AppUser, GetUserListResponse>()
                .ForMember(x => x.FullName, opt => opt.MapFrom(src => src.FullName))
                .ForMember(x => x.Email, opt => opt.MapFrom(src => src.Email))
                .ForMember(x => x.Address, opt => opt.MapFrom(src => src.Address))
                .ForMember(x => x.Country, opt => opt.MapFrom(src => src.Country));
        }
    }
}
