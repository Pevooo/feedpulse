using Api.Core.Features.Authorization.Queries.Response;
using Microsoft.AspNetCore.Identity;

namespace Api.Core.Mapping.Roles
{
    public partial class RoleProfile
    {
        public void GetRoleByIdMappingMethod()
        {
            _ = CreateMap<IdentityRole, GetRoleByIdResponse>();
        }
    }
}
