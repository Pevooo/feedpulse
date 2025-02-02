using Api.Core.Bases;
using Api.Data.DTOS;
using MediatR;

namespace Api.Core.Features.Authorization.Queries.Models
{
    public class ManageUserRolesQuery : IRequest<Response<ManageUserRolesResponse>>
    {
        public string UserId { get; set; }
    }
}
