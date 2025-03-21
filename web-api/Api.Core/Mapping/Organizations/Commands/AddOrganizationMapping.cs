
using Api.Core.Features.Organizations.Commands.Models;
using Api.Data.Entities;

namespace Api.Core.Mapping.Organizations
{
    public partial class OrganizationProfile
    {
        void AddOrganizationMapping()
        {
            _ = CreateMap<AddOrganizationCommand, Organization>()
                .ForMember(x => x.Name, opt => opt.MapFrom(src => src.Name))
                .ForMember(x => x.Description, opt => opt.MapFrom(src => src.Description))
                .ForMember(x => x.PageAccessToken, opt => opt.MapFrom(src => src.PageAccessToken))
                .ForMember(x => x.UserId, opt => opt.MapFrom(src => src.UserId))
                .ForMember(x => x.FacebookId, opt => opt.MapFrom(src => src.FacebookId));
        }
    }
}
