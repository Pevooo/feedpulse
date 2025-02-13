using Api.Core.Bases;
using Api.Core.Features.Authorization.Queries.Response;
using MediatR;

namespace Api.Core.Features.Authorization.Queries.Models
{
    public class GetRoleListQuery : IRequest<Response<List<GetRolesListResponse>>>
    {

    }
}
