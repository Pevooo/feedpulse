using Api.Core.Features.Users.Queries.Response;
using Api.Data.Entities.Identity;

namespace Api.Core.Mapping.Users
{
    public partial class UserProfile
    {
        public void GetUserByIdMapping()
        {
            _ = CreateMap<AppUser, GetUserByIdResponse>();
        }
    }
}
