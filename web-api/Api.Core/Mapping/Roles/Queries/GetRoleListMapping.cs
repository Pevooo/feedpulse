using Api.Core.Features.Authorization.Queries.Response;
using Microsoft.AspNetCore.Identity;

namespace Api.Core.Mapping.Roles
{
    public partial class RoleProfile
    {
        public void GetRoleListMappingMethod()
        {
            _ = CreateMap<IdentityRole, GetRolesListResponse>()
                .ForMember(x => x.Name, opt => opt.MapFrom(src => src.Name))
                .ForMember(x => x.Id, opt => opt.MapFrom(src => src.Id));
        }
    }
}
