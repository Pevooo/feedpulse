using Api.Core.Bases;
using MediatR;

namespace Api.Core.Features.Users.Commands.Models
{
    public class EditUserCommand : IRequest<Response<string>>
    {
        public string Id { get; set; }
        public string FullName { get; set; }
        public string UserName { get; set; }
        public string Email { get; set; }
        public string? Country { get; set; }
        public string? Address { get; set; }
        public string PhoneNumber { get; set; }
        public string Description { get; set; }
    }
}
