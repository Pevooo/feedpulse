using Api.Core.Bases;
using MediatR;

namespace Api.Core.Features.Organizations.Commands.Models
{
    public class AddOrganizationCommand : IRequest<Response<string>>
    {
        public string Name { get; set; }
        public string Description { get; set; }
        public string PageAccessToken { get; set; }
        public string FacebookId { get; set; }
        public string UserId { get; set; }

    }
}
