using Api.Core.Bases;
using Api.Data.Requests;
using MediatR;

namespace Api.Core.Features.Authorization.Commands.Models
{
    public class EditRoleCommand : EditRoleRequest, IRequest<Response<string>>
    {

    }
}
