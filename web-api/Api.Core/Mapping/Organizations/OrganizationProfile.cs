using AutoMapper;

namespace Api.Core.Mapping.Organizations
{
    public partial class OrganizationProfile : Profile
    {
        public OrganizationProfile()
        {
            AddOrganizationMapping();
        }
    }
}
