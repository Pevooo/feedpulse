using AutoMapper;

namespace Api.Core.Mapping.Roles
{
    public partial class RoleProfile : Profile
    {
        public RoleProfile()
        {
            GetRoleByIdMappingMethod();
            GetRoleListMappingMethod();
        }
    }
}
