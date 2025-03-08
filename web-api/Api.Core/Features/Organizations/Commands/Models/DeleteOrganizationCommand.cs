using Api.Core.Bases;
using MediatR;

namespace Api.Core.Features.Organizations.Commands.Models
{
    public class DeleteOrganizationCommand : IRequest<Response<string>>
    {
        public int id { get; set; }
        public DeleteOrganizationCommand(int id)
        {

            this.id = id;
        }
    }
}
