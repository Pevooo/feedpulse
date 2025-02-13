using Api.Core.Features.Users.Commands.Models;
using Api.Data.Entities.Identity;

namespace Api.Core.Mapping.Users
{
    public partial class UserProfile
    {
        public void AddUserMapping()
        {
            _ = CreateMap<AddUserCommand, Organization>()
                .ForMember(x => x.UserName, opt => opt.MapFrom(src => src.UserName))
                .ForMember(x => x.FullName, opt => opt.MapFrom(x => x.FullName))
                .ForMember(x => x.Email, opt => opt.MapFrom(x => x.Email))
                .ForMember(x => x.Country, opt => opt.MapFrom(x => x.Country))
                .ForMember(x => x.PhoneNumber, opt => opt.MapFrom(x => x.PhoneNumber))
                .ForMember(x => x.Address, opt => opt.MapFrom(x => x.Address))
                .ForMember(x => x.Description, opt => opt.MapFrom(x => x.Description));

        }
    }
}
